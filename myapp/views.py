import random
from statistics import quantiles

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
import logging

from django.views.generic import ListView

from myapp.forms import OrderForm
from myapp.models import Product, Review, CartItem, OrderItem, Order

logger = logging.getLogger(__name__)


def index(request):
    products = Product.objects.filter(is_available=True)
    reviews = Review.objects.all().order_by('created_at')[:3]
    return render(request, 'myapp/index.html',
                  {'title': 'Главная страница', 'welcome_message': 'Добро пожаловать', 'products': products,
                   'reviews': reviews})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_available=True)
    return render(request, 'myapp/product_detail.html', {'product': product})


def about(request):
    return render(request, 'myapp/about.html')


def custom_404_view(request, exception):
    return render(request, 'myapp/404.html', status=404)


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


@login_required
def reviews(request):
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        rating = int(request.POST.get('rating', 5))
        if not text:
            messages.error(request, 'Заполните отзыв')

        else:
            Review.objects.create(author=request.username, text=text, rating=rating)
            messages.success(request, 'Ваш отзыв отправлен')
            return redirect('reviews')

    reviews_list = Review.objects.all().order_by('-created_at')
    return render(request, 'myapp/reviews.html', {'reviews': reviews_list, 'title': 'Отзывы о нас'})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    else:
        form = UserCreationForm()

    return render(request, 'myapp/register.html', {'form': form})


@login_required
def order_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    if not cart_items:
        return redirect('cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.order_number = f'{random.randint(1, 100000)}'
            order.save()

            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, quantiy=item.quantity,
                                         price=item.product.price)

            cart_items.delete()

            return redirect('order_success', order_id=order.id)

    else:
        form = OrderForm()

    return render(request, 'myapp/order.html', {'form': form, 'cart_items': cart_items,
                                                'total': total})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, 'myapp/order_success.html', {'order': order})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, 'myapp/order_detail.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'myapp/order_history.html', {'orders': orders})
