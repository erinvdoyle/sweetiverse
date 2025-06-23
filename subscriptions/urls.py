from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.picknmix_signup, name='picknmix_signup'),
    path('manage/', views.manage_subscription, name='manage_subscription'),
    # path('cancel/', views.cancel_subscription, name='cancel_subscription'),
]
