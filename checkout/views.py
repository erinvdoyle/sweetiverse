from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})

    if not bag:
        messages.error(request, "Your SWEETi bag is empty! Don't forget to add your SWEETis")
        return redirect('sweets')

    form = OrderForm()
    context = {
        'order_form': form,
    }
    return render(request, 'checkout/checkout.html', context)
