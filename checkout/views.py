from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import OrderForm
import stripe
from django.conf import settings
from bag.contexts import bag_contents
from .forms import OrderForm
from .models import Order, OrderLineItem
from sweets.models import Sweet
from bag.contexts import bag_contents
import uuid
from decimal import Decimal


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})
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

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.order_number = str(uuid.uuid4()).replace('-', '').upper()
            order.save()

            for item_id, quantity in bag.items():
                try:
                    product = Sweet.objects.get(id=item_id)
                    line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    line_item.save()
                except Sweet.DoesNotExist:
                    messages.error(request, (
                        "One of the sweets in your bag wasn't found. "
                        "Please call us for assistance!"
                    ))
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please check your information.')
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "Your bag is empty")
            return redirect(reverse('sweets'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key

        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'bag_items': current_bag['bag_items'],
        'total': current_bag['total'],
        'grand_total': current_bag['grand_total'],
        'delivery': current_bag['delivery'],
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """ Handle successful checkouts """
    order = get_object_or_404(Order, order_number=order_number)

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation email \
        will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    context = {
        'order': order,
    }

    return render(request, 'checkout/checkout_success.html', context)
