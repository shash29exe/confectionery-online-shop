from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
        Класс продуктов в админ панели
    """

    list_display = ('name', 'slug', 'price', 'description', 'is_available', 'created_at')
    list_filter = ('is_available', 'created_at', 'price')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
