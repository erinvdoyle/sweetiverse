from django.shortcuts import render, redirect
from .forms import SubscriptionForm
from django.db.models import Count
from sweets.models import Sweet
from .forms import PickNMixForm
from .models import PickNMixSubscription
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            sub, created = SubscriptionProfile.objects.get_or_create(user=request.user)
            sub.candy_types = ",".join(form.cleaned_data['candy_types'])
            sub.flavor_preferences = ",".join(form.cleaned_data['flavor_preferences'])
            sub.frequency = form.cleaned_data['frequency']
            sub.save()

            subscription_product = SubscriptionProduct.objects.first()
            bag = request.session.get('bag', {})
            bag[str(subscription_product.id)] = 1
            request.session['bag'] = bag

            return redirect('checkout')
    else:
        form = SubscriptionForm()
        top_flavors = Sweet.objects.values_list('flavor', flat=True).annotate(count=Count('flavor')).order_by('-count')[:5]
        form.fields['flavor_preferences'].choices = [(fl, fl) for fl in top_flavors]

    return render(request, 'subscriptions/subscribe.html', {'form': form})


def picknmix_signup(request):
    form = PickNMixForm()
    top_flavors = Sweet.objects.values('flavor').annotate(count=Count('flavor')).order_by('-count')[:5]
    form.fields['flavor_preferences'].choices = [(f['flavor'], f['flavor']) for f in top_flavors]

    if request.method == 'POST':
        form = PickNMixForm(request.POST)
        form.fields['flavor_preferences'].choices = [(f['flavor'], f['flavor']) for f in top_flavors]
        if form.is_valid():
            picknmix_data = {
                'sweet_types': form.cleaned_data['sweet_types'],
                'flavor_preferences': form.cleaned_data['flavor_preferences'],
                'explorer': form.cleaned_data['explorer'],
                'delivery_frequency': form.cleaned_data['delivery_frequency'],
            }

            request.session['picknmix_data'] = picknmix_data

            subscription_product = Sweet.objects.filter(name__icontains='Pick').first()

            if subscription_product:
                bag = request.session.get('bag', {})
                bag[str(subscription_product.id)] = {
                    'quantity': 1,
                    'subscription_details': picknmix_data
                }
                request.session['bag'] = bag
                return redirect('checkout')
            else:
                messages.error(request, "Subscription product not found.")

    return render(request, 'subscriptions/picknmix_signup.html', {'form': form})


@login_required
def manage_subscription(request):
    subscriptions = PickNMixSubscription.objects.filter(user=request.user)

    if request.method == 'POST':
        sub_id = request.POST.get('sub_id')
        action = request.POST.get('action')
        subscription = subscriptions.filter(id=sub_id).first()

        if not subscription:
            messages.error(request, "Subscription not found.")
            return redirect('manage_subscription')

        try:
            if action == 'pause':
                if subscription.stripe_subscription_id:
                    stripe.Subscription.modify(
                        subscription.stripe_subscription_id,
                        cancel_at_period_end=True
                    )
                subscription.active = False
                subscription.save()
                messages.success(request, "Subscription paused.")

            elif action == 'resume':
                if subscription.stripe_subscription_id:
                    stripe.Subscription.modify(
                        subscription.stripe_subscription_id,
                        cancel_at_period_end=False
                    )
                subscription.active = True
                subscription.save()
                messages.success(request, "Subscription resumed.")

            elif action == 'cancel':
                if subscription.stripe_subscription_id:
                    stripe.Subscription.delete(subscription.stripe_subscription_id)
                subscription.delete()
                messages.success(request, "Subscription cancelled.")
        except stripe.error.StripeError as e:
            messages.error(request, f"Stripe error: {e.user_message}")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

        return redirect('manage_subscription')

    return render(request, 'subscriptions/manage_subscription.html', {
        'subscriptions': subscriptions
    })