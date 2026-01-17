from django.shortcuts import render, get_object_or_404
import logging

from myapp.models import Product, Review

logger = logging.getLogger(__name__)


def index(request):
    products = Product.objects.filter(is_available=True)
    reviews = Review.objects.all().order_by('created_at')[:3]
    return render(request, 'myapp/index.html',
                  {'title': 'Главная страница', 'welcome_message': 'Добро пожаловать', 'products': products, 'reviews': reviews})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    return render(request, 'myapp/product_detail.html', {'product': product})

def about(request):
    return render(request, 'myapp/about.html')