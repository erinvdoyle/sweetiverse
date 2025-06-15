from django.urls import path
from . import views


urlpatterns = [
    path('sweets/', views.sweets_list, name='sweets'),
    path('search/', views.search_results, name='search_results'),
    path('add/', views.add_sweet, name='add_sweet'),
    path('edit/<uuid:sweet_id>/', views.edit_sweet, name='edit_sweet'),
    path('delete/<uuid:sweet_id>/', views.delete_sweet, name='delete_sweet'),
    path('<uuid:sweet_id>/', views.sweet_detail, name='sweet_detail'),
]
