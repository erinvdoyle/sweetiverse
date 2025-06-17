from django.contrib import admin
from .models import PickNMixSubscription


@admin.register(PickNMixSubscription)
class PickNMixSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'delivery_frequency',
        'active',
        'next_billing_date',
        'stripe_price_id',
    )
    list_filter = ('delivery_frequency', 'active')
    search_fields = ('user__username',)