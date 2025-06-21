from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from sweets.models import Sweet

def bag_contents(request):
    bag_items = []
    total = Decimal('0.00')
    sweet_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        sweet = get_object_or_404(Sweet, pk=item_id)

        if isinstance(item_data, int):
            quantity = item_data
            subscription_details = None
        else:
            quantity = item_data.get('quantity', 1)
            subscription_details = item_data.get('subscription_details', None)

        total += quantity * sweet.price
        sweet_count += quantity

        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'sweet': sweet,
            'subscription_details': subscription_details,
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = Decimal('0.00')
        free_delivery_delta = 0

    grand_total = total + delivery

    context = {
        'bag_items': bag_items,
        'total': total,
        'sweet_count': sweet_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context

