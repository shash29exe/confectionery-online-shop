from django.shortcuts import render
import logging

from myapp.models import Product, Review

logger = logging.getLogger(__name__)

def index(request):
    featured_products = Product.objects.filter(is_available=True)[:4]
    latest_reviews = Review.objects.all().order_by('created_at')[:3]
    return render(request, 'myapp/index.html',
                  {'title': 'Главная страница', 'welcome_message': 'Добро пожаловать',
                   'featured_products': featured_products, 'latest_reviews': latest_reviews})
