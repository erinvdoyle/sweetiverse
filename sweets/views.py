from django.shortcuts import render, get_object_or_404, redirect
from .models import Sweet, Category
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect, reverse


def search_results(request):
    """ View to show all sweets, with search, sort, filter, and pagination """
    sweets = Sweet.objects.all()
    query = request.GET.get('q')
    sort = request.GET.get('sort')
    category_filter = request.GET.get('category')

    if query is not None:
        if not query.strip():
            messages.error(request, "Oops! You forgot to type something")
            return redirect('sweets')
        sweets = sweets.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if category_filter:
        sweets = sweets.filter(categories__name=category_filter)

    sort_options = {
        'name': 'name',
        'price': 'price',
        'rating': 'rating',
        'type': 'type__friendly_name',
    }
    if sort:
        sort_field = sort_options.get(sort, 'name')
        sweets = sweets.order_by(sort_field)

    paginator = Paginator(sweets, 4)
    page = request.GET.get('page')
    try:
        paged_sweets = paginator.page(page)
    except PageNotAnInteger:
        paged_sweets = paginator.page(1)
    except EmptyPage:
        paged_sweets = paginator.page(paginator.num_pages)

    categories = Category.objects.all()

    context = {
        'sweets': paged_sweets,
        'search_term': query,
        'current_category': category_filter,
        'categories': categories,
    }

    return render(request, 'home/search_results.html', context)


def sweet_detail(request, sweet_id):
    """
    View to show an individual sweet's detail.
    """
    sweet = get_object_or_404(Sweet, pk=sweet_id)
    return render(request, 'sweets/sweet_detail.html', {'sweet': sweet})


def sweets_list(request):
    """View to show all sweets"""
    sweets = Sweet.objects.all()
    return render(request, 'sweets/sweets.html', {'sweets': sweets})
