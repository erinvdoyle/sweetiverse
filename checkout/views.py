from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
import stripe
from django.conf import settings
from bag.contexts import bag_contents

def checkout(request):
    bag = request.session.get('bag', {})

    if not bag:
        messages.error(request, "Your SWEETi bag is empty! Don't forget to add your SWEETis")
        return redirect('sweets')

    order_form = OrderForm()

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    context = {
        'order_form': order_form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
        'bag_items': current_bag['bag_items'],
        'total': current_bag['total'],
        'grand_total': current_bag['grand_total'],
        'delivery': current_bag['delivery'],
    }
    
    if not settings.STRIPE_PUBLIC_KEY:
        messages.warning(request, 'Stripe public key is missing. Did you set it in your env.py?')

    return render(request, 'checkout/checkout.html', context)
