from django.contrib import admin
from .models import Product, Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
        Класс продуктов в админ панели
    """

    list_display = ('name', 'slug', 'price', 'description', 'is_available', 'created_at')
    list_filter = ('is_available', 'created_at', 'price')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
        Класс отзывов в админ панели
    """

    list_display = ('author', 'rating', 'created_at', 'is_approved')
    list_filter = ('rating', 'created_at', 'is_approved')
    search_fields = ('author', 'rating', 'created_at')

    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)

    approve_reviews.short_description = 'Одобрить выбранные отзывы'