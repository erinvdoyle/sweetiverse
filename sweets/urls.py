from django.urls import path
from . import views


urlpatterns = [
    path('sweets/', views.sweets_list, name='sweets'),
    path('search/', views.search_results, name='search_results'),
    path('<uuid:sweet_id>/', views.sweet_detail, name='sweet_detail'),
]
