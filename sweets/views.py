from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Sweet, Category
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from urllib.parse import urlencode
from .forms import SweetForm
from django.contrib.auth.decorators import login_required


def search_results(request):
    sweets = Sweet.objects.all()
    query = request.GET.get('q')
    sort = request.GET.get('sort')
    category_param = request.GET.get('category')

    category_names = []
    current_categories = []

    if query:
        if not query.strip():
            messages.error(request, "Oops! You forgot to type something")
            return redirect(reverse('sweets'))
        sweets = sweets.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category_param:
        category_names = [name.strip() for name in category_param.split(',') if name.strip()]
        sweets = sweets.filter(categories__name__in=category_names).distinct()
        current_categories = Category.objects.filter(name__in=category_names)

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

    query_params = request.GET.copy()
    query_params.pop('page', None)
    base_query = urlencode(query_params)

    categories = Category.objects.all()

    context = {
        'sweets': paged_sweets,
        'search_term': query,
        'categories': categories,
        'current_categories': current_categories,
        'category_names': ','.join(category_names),
        'base_query': base_query,
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
    sort = request.GET.get('sort')
    category_param = request.GET.get('category')

    current_categories = []
    if category_param:
        category_names = [name.strip() for name in category_param.split(',') if name.strip()]
        sweets = sweets.filter(categories__name__in=category_names).distinct()
        current_categories = Category.objects.filter(name__in=category_names)
    else:
        category_names = []

    sort_options = {
        'price': 'price',
        'rating': 'rating',
        'type': 'type__friendly_name',
    }
    if sort:
        sort_field = sort_options.get(sort)
        if sort_field:
            sweets = sweets.order_by(sort_field)

    categories = Category.objects.all()

    context = {
        'sweets': sweets,
        'sort': sort,
        'categories': categories,
        'current_categories': current_categories,
        'category_names': ','.join(category_names),
    }

    return render(request, 'sweets/sweets.html', context)


def add_sweet(request):
    if not request.user.is_superuser:
        messages.error(request, "Only store owners can do that.")
        return redirect('home')

    if request.method == 'POST':
        form = SweetForm(request.POST, request.FILES)
        if form.is_valid():
            sweet = form.save()
            messages.success(request, "Sweet added successfully!")
            return redirect('sweet_detail', sweet_id=sweet.id)
        else:
            messages.error(request, "Oops! Please check the form for errors.")
    else:
        form = SweetForm()

    context = {
        'form': form
    }
    return render(request, 'sweets/add_sweet.html', context)


def edit_sweet(request, sweet_id):
    if not request.user.is_superuser:
        messages.error(request, "Only store owners can edit sweets.")
        return redirect('home')

    sweet = get_object_or_404(Sweet, pk=sweet_id)

    if request.method == 'POST':
        form = SweetForm(request.POST, request.FILES, instance=sweet)
        if form.is_valid():
            form.save()
            messages.success(request, "Sweet updated successfully.")
            return redirect('sweet_detail', sweet_id=sweet.id)
        else:
            messages.error(request, "Error updating sweet. Please check form.")
    else:
        form = SweetForm(instance=sweet)

    context = {
        'form': form,
        'sweet': sweet
    }
    return render(request, 'sweets/edit_sweet.html', context)


@login_required
def delete_sweet(request, sweet_id):
    if not request.user.is_superuser:
        messages.error(request, "Only store owners can delete sweets.")
        return redirect('home')

    sweet = get_object_or_404(Sweet, pk=sweet_id)
    sweet.delete()
    messages.success(request, f'{sweet.name} has been deleted.')
    return redirect('sweets')
