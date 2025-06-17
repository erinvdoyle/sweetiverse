from django.contrib import admin
from .models import Sweet, Type, Category
from django.db import models

# Register your models here.


class SweetAdmin(admin.ModelAdmin):
    list_display = (
        'sku', 'name', 'price', 'rating', 'in_stock', 'on_sale', 'image',
    )
    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')


class TypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')
    

admin.site.register(Sweet, SweetAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Type, TypeAdmin)
