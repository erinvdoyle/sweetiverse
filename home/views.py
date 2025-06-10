from django.shortcuts import render
from sweets.models import Sweet

# Create your views here.


def index(request):
    """A view to return the index page"""
    return render(request, 'home/index.html')


# def search_results(request):
#     query = request.GET.get('q')
#     sweets = Sweet.objects.filter(name__icontains=query)
#     return render(request, 'home/search_results.html', {'query': query, 'sweets': sweets})
