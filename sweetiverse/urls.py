from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from sweetiverse import views as core_views
from sweets import views as sweets_views
from allauth.account.views import confirm_email
from django.views.generic import TemplateView
from sweetiverse.views import CustomConfirmEmailView

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('bag/', include('bag.urls')),
    path('', include('home.urls')),
    path('sweets/', include('sweets.urls')),
    path('search/', sweets_views.search_results, name='search_results'),
    path('checkout/', include('checkout.urls')),
    path('profile/', include('profiles.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml")),
    path('accounts/confirm-email/<key>/', CustomConfirmEmailView.as_view(), name='account_confirm_email'),
]

if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
