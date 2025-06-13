from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)
