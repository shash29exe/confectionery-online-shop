from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
import logging

from django.views.generic import ListView

from myapp.models import Product, Review, CartItem

logger = logging.getLogger(__name__)


def index(request):
    products = Product.objects.filter(is_available=True)
    reviews = Review.objects.all().order_by('created_at')[:3]
    return render(request, 'myapp/index.html',
                  {'title': 'Главная страница', 'welcome_message': 'Добро пожаловать', 'products': products,
                   'reviews': reviews})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    return render(request, 'myapp/product_detail.html', {'product': product})


def about(request):
    return render(request, 'myapp/about.html')


class ProductListView(ListView):
    model = Product
    template_name = 'myapp/products.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        return Product.objects.filter(is_available=True).order_by('-created_at')


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'myapp/cart.html',
                  {'cart_items': cart_items, 'total': total,
                   'cart_items_count': cart_items.count()})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        user=request.user,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'{product.name} добавлен в корзину')
    return redirect('product')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()

    return redirect('cart')