from django.shortcuts import render
from .models import Sweet


def all_sweets(request):
    """ A view to return all sweets """
    sweets = Sweet.objects.all()
    context = {
        'sweets': sweets,
    }
    return render(request, 'sweets/sweets.html', context)

