from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import OrderForm
import stripe
from django.conf import settings
from bag.contexts import bag_contents
from .forms import OrderForm
from .models import Order, OrderLineItem, DiscountCode
from sweets.models import Sweet
from bag.contexts import bag_contents
import uuid
from decimal import Decimal
import json
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from subscriptions.models import PickNMixSubscription
from subscriptions.utils import create_stripe_subscription
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    current_bag = bag_contents(request)
    total = current_bag['total']
    delivery = current_bag['delivery']
    discount = Decimal('0.00')
    promo_code_input = ""
    discount_obj = None

    if request.method == 'POST':
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'city': request.POST['city'],
            'postcode': request.POST['postcode'],
            'county': request.POST['county'],
            'country': request.POST['country'],
        }

        promo_code_input = request.POST.get('promo_code', '').strip().upper()
        if promo_code_input:
            try:
                discount_obj = DiscountCode.objects.get(code=promo_code_input, active=True)
                if discount_obj.usage_limit is None or discount_obj.used_count < discount_obj.usage_limit:
                    if discount_obj.is_percentage:
                        discount = total * (discount_obj.amount / 100)
                    else:
                        discount = discount_obj.amount
                    total -= discount
                    messages.success(request, f"Promo code '{promo_code_input}' applied! 🎉")
                else:
                    messages.error(request, "This discount code has expired.")
            except DiscountCode.DoesNotExist:
                messages.error(request, "Invalid discount code.")

        grand_total = total + delivery
        stripe_total = round(grand_total * 100)
        stripe.api_key = stripe_secret_key

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.discount = discount
            order.promo_code_used = promo_code_input
            order.save()
            order.update_total()

            if request.user.is_authenticated:
                try:
                    profile = UserProfile.objects.get(user=request.user)
                    order.user_profile = profile
                except UserProfile.DoesNotExist:
                    pass

            order.save()

            for item_id, item_data in bag.items():
                try:
                    sweet = Sweet.objects.get(id=item_id)
                    quantity = item_data if isinstance(item_data, int) else item_data.get('quantity', 1)
                    subscription_details = None if isinstance(item_data, int) else item_data.get('subscription_details')

                    OrderLineItem.objects.create(
                        order=order,
                        product=sweet,
                        quantity=quantity,
                        subscription_details=subscription_details,
                    )
                except Sweet.DoesNotExist:
                    messages.error(request, "One of the sweets in your bag wasn't found.")
                    order.delete()
                    return redirect(reverse('view_bag'))

            if promo_code_input and discount > 0 and discount_obj:
                try:
                    discount_obj.used_count += 1
                    discount_obj.save()
                except Exception:
                    pass

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please check your information.')

    else:
        if not bag:
            messages.error(request, "Your bag is empty")
            return redirect(reverse('sweets'))

        grand_total = total + delivery
        stripe_total = round(grand_total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'bag_items': current_bag['bag_items'],
        'total': total,
        'delivery': delivery,
        'grand_total': total + delivery,
        'discount': discount,
        'promo_code': promo_code_input,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """Handle successful checkouts"""
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

        if request.session.get('save_info'):
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_city': order.city,
                'default_postcode': order.postcode,
                'default_county': order.county,
                'default_country': order.country,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

        try:
            from subscriptions.models import PickNMixSubscription
            from sweets.models import Sweet

            subscription_data = request.session.pop('picknmix_data', None)
            if subscription_data:
                picknmix_sweet = Sweet.objects.filter(name__icontains="Pick").first()
                subscription_in_order = OrderLineItem.objects.filter(
                    order=order, product=picknmix_sweet
                ).exists()

                if subscription_in_order:
                    frequency = subscription_data['delivery_frequency']
                    next_billing = (
                        timezone.now() + timedelta(weeks=1)
                        if frequency == 'weekly'
                        else timezone.now() + timedelta(weeks=2)
                        if frequency == 'biweekly'
                        else timezone.now() + timedelta(days=30)
                    )

                    PickNMixSubscription.objects.update_or_create(
                        user=request.user,
                        defaults={
                            'sweet_types': ", ".join(subscription_data['sweet_types']),
                            'flavor_preferences': ", ".join(subscription_data['flavor_preferences']),
                            'explorer': subscription_data['explorer'],
                            'delivery_frequency': frequency,
                            'active': True,
                            'next_billing_date': next_billing,
                        }
                    )
        except Exception as e:
            messages.warning(request, f"Note: Subscription was not created automatically. {str(e)}")

    request.session.pop('promo_code', None)

    subject = f"SWEETiVERSE Order Confirmation – {order.order_number}"
    body = render_to_string('checkout/emails/confirmation_email_body.txt', {
        'order': order,
        'contact_email': settings.DEFAULT_FROM_EMAIL
    })

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
    )

    messages.success(request, f'Order successfully processed! '
        f'Your order number is {order.order_number}. A confirmation email '
        f'has been sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    context = {
        'order': order,
        'from_profile': request.GET.get('from_profile') == '1',
        'on_profile_page': False,
    }

    return render(request, 'checkout/checkout_success.html', context)


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed right now.')
        return HttpResponse(content=e, status=400)