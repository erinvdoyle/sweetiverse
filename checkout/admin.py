from django.contrib import admin
from .models import Order, OrderLineItem, DiscountCode


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)
    fields = ('product', 'quantity', 'lineitem_total', 'subscription_details')


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('order_number', 'date', 'delivery_cost',
                       'order_total', 'discount', 'promo_code_used',
                       'grand_total', 'original_bag', 'stripe_pid')

    fields = ('order_number', 'user_profile', 'full_name', 'email', 'phone_number',
              'street_address1', 'street_address2', 'city', 'postcode',
              'county', 'country', 'date', 'discount', 'promo_code_used',
              'delivery_cost', 'order_total', 'grand_total')

    list_display = ('order_number', 'full_name', 'user_profile', 'date',
                    'order_total', 'discount', 'promo_code_used',
                    'delivery_cost', 'grand_total')

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
admin.site.register(DiscountCode)
