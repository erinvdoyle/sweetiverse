from django.shortcuts import render, get_object_or_404, redirect
from sweets.models import Sweet
from .models import WishlistItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order

@login_required
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
    else:
        form = UserProfileForm(instance=profile)

    orders = profile.orders.all()

    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, 'profiles/profile.html', context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, f'This is a past confirmation for order number { order_number }. A confirmation email was sent on the order date.')

    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, 'checkout/checkout_success.html', context)


@login_required
def add_to_wishlist(request, sweet_id):
    sweet = get_object_or_404(Sweet, pk=sweet_id)
    WishlistItem.objects.get_or_create(user=request.user, sweet=sweet)
    messages.success(request, f'{sweet.name} added to your wishlist 💖')
    return redirect(request.META.get('HTTP_REFERER', 'sweet_detail'))


@login_required
def remove_from_wishlist(request, sweet_id):
    sweet = get_object_or_404(Sweet, pk=sweet_id)
    WishlistItem.objects.filter(user=request.user, sweet=sweet).delete()
    messages.info(request, f'{sweet.name} removed from your wishlist 💔')
    return redirect(request.META.get('HTTP_REFERER', 'sweet_detail'))


@login_required
def wishlist_view(request):
    wishlist = WishlistItem.objects.filter(user=request.user).select_related('sweet')
    return render(request, 'profiles/wishlist.html', {'wishlist': wishlist})