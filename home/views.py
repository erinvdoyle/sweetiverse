from django.shortcuts import render
from django.db.models import Count
from sweets.models import Sweet
from profiles.models import WishlistItem
# Create your views here.


def index(request):
    """A view to return the index page"""
    popular_sweets = (
        Sweet.objects.annotate(wishlist_count=Count('wishlisted_by'))
        .order_by('-wishlist_count')[:4]
    )

    context = {
        'popular_sweets': popular_sweets,
    }
    return render(request, 'home/index.html', context)


def faq(request):
    return render(request, 'home/faq.html')
