from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('order_number', 'date', 'delivery_cost',
                       'order_total', 'grand_total', 'original_bag', 'stripe_pid')
    fields = ('order_number', 'full_name', 'email', 'phone_number',
              'street_address1', 'street_address2', 'city', 'postcode',
              'county', 'country', 'date', 'delivery_cost',
              'order_total', 'grand_total')

    list_display = ('order_number', 'full_name', 'date',
                    'order_total', 'delivery_cost', 'grand_total',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
