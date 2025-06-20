from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('faq/', views.faq, name='faq'),
    path("privacy/", TemplateView.as_view(template_name="home/privacy.html"), name="privacy"),
]
