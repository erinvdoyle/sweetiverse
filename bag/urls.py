from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<sweet_id>/', views.add_to_bag, name='add_to_bag'),
    path('adjust/<sweet_id>/', views.adjust_bag, name='adjust_bag'),
    path('remove/<sweet_id>/', views.remove_from_bag, name='remove_from_bag'),
    path('save/<uuid:sweet_id>/', views.save_for_later, name='save_for_later'),
]