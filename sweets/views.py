from django.shortcuts import render
from sweets.models import Sweet

# Create your views here.


def all_sweets(request):
    sweets = Sweet.objects.all()
    return render(request, 'sweets/sweets.html', {'sweets': sweets})
