from django.shortcuts import get_object_or_404
from sweets.models import Sweet
from decimal import Decimal
from django.conf import settings


def bag_contents(request):
    bag_items = []
    total = Decimal('0.00')
    sweeti_count = 0
    lowest_price = None
    discount = Decimal('0.00')

    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        sweet = get_object_or_404(Sweet, pk=item_id)

        if isinstance(item_data, int):
            quantity = item_data
            subscription_details = None
        else:
            quantity = item_data.get('quantity', 1)
            subscription_details = item_data.get('subscription_details', None)

        line_total = quantity * sweet.price
        total += line_total
        sweeti_count += quantity

        for _ in range(quantity):
            if lowest_price is None or sweet.price < lowest_price:
                lowest_price = sweet.price

        bag_items.append({
            'sweet_id': item_id,
            'quantity': quantity,
            'sweet': sweet,
            'subscription_details': subscription_details,
        })

    sweetistravaganza_applied = False
    if sweeti_count >= 4:
        if lowest_price:
            discount = lowest_price
            total -= discount
        sweetistravaganza_applied = True

    delivery = Decimal('3.95') if total < 25 else Decimal('0.00')
    grand_total = total + delivery

    return {
        'bag_items': bag_items,
        'total': total,
        'sweeti_count': sweeti_count,
        'delivery': delivery,
        'grand_total': grand_total,
        'sweetistravaganza_discount': discount,
        'sweetistravaganza_applied': sweetistravaganza_applied,
        'sweetistravaganza_needed': max(0, 4 - sweeti_count),
    }
