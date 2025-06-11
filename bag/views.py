from django.shortcuts import render, redirect, get_object_or_404
from sweets.models import Sweet


# Create your views here.


def view_bag(request):
    """ View to render the sweeti shopping bag page """
    return render(request, 'bag/bag.html')


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
    return redirect(redirect_url)