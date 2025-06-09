from django.shortcuts import render, get_object_or_404
from .models import Sweet


def all_sweets(request):
    """ A view to return all sweets """
    sweets = Sweet.objects.all()
    context = {
        'sweets': sweets,
    }
    return render(request, 'sweets/sweets.html', context)


def sweet_detail(request, sweet_id):
    """
    View to show an individual sweet's detail.
    """
    sweet = get_object_or_404(Sweet, pk=sweet_id)
    return render(request, 'sweets/sweet_detail.html', {'sweet': sweet})
