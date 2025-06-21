from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Sweet, Category, SweetReview, Type
from django.db.models import Q, Count
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from urllib.parse import urlencode
from .forms import SweetForm, SweetReviewForm, SweetiSelectorForm
from django.contrib.auth.decorators import login_required
from checkout.models import OrderLineItem
from datetime import timedelta
from django.utils import timezone


EXCLUDED_SWEETS = ["Sweetistravaganza Mystery Sweeti", "PickNMix Subscription Box"]


def search_results(request):
    sweets = Sweet.objects.exclude(name__in=EXCLUDED_SWEETS)
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

    sweets = sweets.exclude(name__in=EXCLUDED_SWEETS)

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

    pill_urls = []
    for cat in current_categories:
        remaining = [c.name for c in current_categories if c != cat]
        qs = request.GET.copy()
        if remaining:
            qs['category'] = ','.join(remaining)
        else:
            qs.pop('category', None)
        pill_urls.append(qs.urlencode())

    categories = Category.objects.all()

    context = {
        'sweets': paged_sweets,
        'search_term': query,
        'categories': categories,
        'current_categories': current_categories,
        'category_names': ','.join(category_names),
        'base_query': base_query,
        'pill_urls': pill_urls,
    }

    return render(request, 'home/search_results.html', context)


@login_required
def sweet_detail(request, sweet_id):
    sweet = get_object_or_404(Sweet, pk=sweet_id)
    user = request.user

    is_wishlisted = user.wishlist_items.filter(sweet=sweet).exists()

    has_purchased = OrderLineItem.objects.filter(
        order__user_profile=user.userprofile, product=sweet
    ).exists()

    review_instance = SweetReview.objects.filter(sweet=sweet, user=user).first()
    has_reviewed = bool(review_instance)

    if request.method == 'POST' and has_purchased:
        form = SweetReviewForm(request.POST, instance=review_instance)
        if form.is_valid():
            review = form.save(commit=False)
            review.sweet = sweet
            review.user = user
            review.save()
            sweet.update_rating()
            messages.success(request, "Review submitted!" if not review_instance else "Review updated!")
            return redirect('sweet_detail', sweet_id=sweet.id)
    else:
        form = SweetReviewForm(instance=review_instance)

    reviews = sweet.reviews.all().order_by('-created_at')

    recommendations = Sweet.objects.none()

    category_matches = Sweet.objects.filter(
        Q(categories__in=sweet.categories.all())
    ).exclude(id=sweet.id).exclude(name__in=EXCLUDED_SWEETS).distinct()

    recommendations = category_matches

    if recommendations.count() < 4 and sweet.type:
        type_matches = Sweet.objects.filter(type=sweet.type).exclude(
            id__in=[sweet.id] + list(recommendations.values_list('id', flat=True))
        ).exclude(name__in=EXCLUDED_SWEETS)
        recommendations = recommendations | type_matches

    if recommendations.count() < 4:
        flavor_matches = Sweet.objects.filter(flavor__iexact=sweet.flavor).exclude(
            id__in=[sweet.id] + list(recommendations.values_list('id', flat=True))
        ).exclude(name__in=EXCLUDED_SWEETS)
        recommendations = recommendations | flavor_matches

    if recommendations.count() < 4:
        fill_needed = 4 - recommendations.count()
        top_rated = Sweet.objects.exclude(
            id__in=[sweet.id] + list(recommendations.values_list('id', flat=True))
        ).exclude(name__in=EXCLUDED_SWEETS).order_by('-rating')[:fill_needed]
        recommendations = recommendations | top_rated

    recommendations = recommendations.distinct()[:4]

    context = {
        'sweet': sweet,
        'is_wishlisted': is_wishlisted,
        'form': form,
        'has_purchased': has_purchased,
        'has_reviewed': has_reviewed,
        'reviews': reviews,
        'recommendations': recommendations,
    }
    return render(request, 'sweets/sweet_detail.html', context)


def sweets_list(request):
    sweets = Sweet.objects.exclude(name__in=EXCLUDED_SWEETS)
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

    sweets = sweets.exclude(name__in=EXCLUDED_SWEETS)

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


@login_required
def delete_review(request, sweet_id):
    review = get_object_or_404(SweetReview, sweet_id=sweet_id, user=request.user)

    if request.method == "POST":
        review.delete()
        messages.success(request, "Your review has been deleted.")
        return redirect('sweet_detail', sweet_id=sweet_id)

    messages.warning(request, "Invalid request.")
    return redirect('sweet_detail', sweet_id=sweet_id)


def sweetiselector(request):
    form = SweetiSelectorForm(request.GET or None)
    all_sweets = Sweet.objects.filter(in_stock=True).exclude(name__in=EXCLUDED_SWEETS)

    filtered_sweets = all_sweets

    if request.GET and form.is_valid():
        data = form.cleaned_data

        if data['fruity_vs_chocolate']:
            chocolate_cat = Category.objects.filter(name__iexact='chocolate').first()
            if chocolate_cat:
                filtered_sweets = filtered_sweets.filter(categories=chocolate_cat)
        else:
            fruity_type = Type.objects.filter(name__iexact='fruity').first()
            if fruity_type:
                filtered_sweets = filtered_sweets.filter(type=fruity_type)

        base_pool = filtered_sweets

        texture_cat_name = 'chewy-candy' if data['texture'] else 'hard-candy'
        texture_cat = Category.objects.filter(name__iexact=texture_cat_name).first()
        if texture_cat:
            filtered_sweets = filtered_sweets.filter(categories=texture_cat)

        last_month = timezone.now() - timedelta(days=30)
        if data['flavor_age']:
            filtered_sweets = filtered_sweets.filter(created__lt=last_month)
        else:
            filtered_sweets = filtered_sweets.filter(created__gte=last_month)

        filtered_sweets = filtered_sweets.annotate(wishlist_count=Count('wishlisted_by'))
        if data['popularity']:
            filtered_sweets = filtered_sweets.order_by('wishlist_count') 
        else:
            filtered_sweets = filtered_sweets.order_by('-wishlist_count')

        filtered_sweets = filtered_sweets.distinct()
        selected_sweets = list(filtered_sweets[:3])

        if len(selected_sweets) < 3:
            remaining = 3 - len(selected_sweets)
            base_fallback = base_pool.exclude(id__in=[s.id for s in selected_sweets])
            base_fallback = base_fallback.order_by('?')[:remaining]
            selected_sweets.extend(base_fallback)

    else:
        selected_sweets = []

    context = {
        'form': form,
        'selected_sweets': selected_sweets,
        'suggestions': bool(selected_sweets),
    }
    return render(request, 'sweets/sweetiselector.html', context)
