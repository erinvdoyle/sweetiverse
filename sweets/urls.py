from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_sweets, name='sweets'),
    path('<uuid:sweet_id>/', views.sweet_detail, name='sweet_detail'),
]
