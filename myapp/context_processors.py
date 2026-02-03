from .models import CartItem
from django.db.models import Sum, F


def cart_context(request):

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)

        items_count = cart_items.aggregate(
            total_quantity=Sum('quantity')
        )['total_quantity'] or 0

        total_price = cart_items.aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total'] or 0
    else:
        items_count = 0
        total_price = 0

    return {
        'cart_items_count': items_count,
        'cart_total_price': total_price,
    }
