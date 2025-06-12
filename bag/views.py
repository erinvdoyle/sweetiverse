from django.shortcuts import render, redirect, get_object_or_404
from sweets.models import Sweet
from django.contrib import messages
from .context_processors import bag_contents
from django.http import HttpResponse, JsonResponse


# Create your views here.


def view_bag(request):
    """ View to render the sweeti shopping bag page """
    context = bag_contents(request)

    if context.get('sweetistravaganza_applied'):
        if not request.session.get('sweetistravaganza_message_shown'):
            messages.success(request, "🎁 SWEETiStravaganza: 1 Sweeti is FREE!")
            request.session['sweetistravaganza_message_shown'] = True
    else:
        request.session['sweetistravaganza_message_shown'] = False

    return render(request, 'bag/bag.html', context)


def add_to_bag(request, sweet_id):
    """
    Add a quantity of the specified sweet to the shopping bag.
    """
    sweet = get_object_or_404(Sweet, pk=sweet_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if sweet_id in bag:
        bag[sweet_id] += quantity
    else:
        bag[sweet_id] = quantity

    request.session['bag'] = bag
    messages.success(request, f"🍬 Added {quantity} × {sweet.name} to your bag!")
    return redirect(redirect_url)


def adjust_bag(request, sweet_id):
    """
    Adjust the quantity of the specified sweet to the specified amount.
    """
    try:
        quantity = int(request.POST.get('quantity'))
        if quantity < 1 or quantity > 99:
            messages.warning(request, 'Please enter a quantity between 1 and 99.')
            return redirect('view_bag')
    except (TypeError, ValueError):
        messages.error(request, 'Invalid quantity provided.')
        return redirect('view_bag')

    bag = request.session.get('bag', {})
    sweet = get_object_or_404(Sweet, pk=sweet_id)

    if quantity > 0:
        bag[sweet_id] = quantity
        messages.success(request, f"🔁 Updated {sweet.name} quantity to {quantity}.")
    else:
        bag.pop(sweet_id, None)
        messages.success(request, f"❌ Removed {sweet.name} from your bag.")

    request.session['bag'] = bag
    return redirect('view_bag')



def remove_from_bag(request, sweet_id):
    """
    Remove the item from the shopping bag.
    """
    try:
        bag = request.session.get('bag', {})
        bag.pop(sweet_id, None)
        request.session['bag'] = bag
        request.session.modified = True
        sweet = get_object_or_404(Sweet, pk=sweet_id)


        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(status=200)
        else:
            messages.success(request, f"❌ Removed {sweet.name} from your bag.")
            return redirect('view_bag')
    except Exception as e:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': str(e)}, status=500)
        else:
            messages.error(request, f'Error removing item: {e}')
            return redirect('view_bag')


def save_for_later(request, sweet_id):
    messages.info(request, "Save for later is coming soon! 💖")
    return redirect('view_bag')
