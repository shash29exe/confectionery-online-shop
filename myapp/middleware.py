import logging
import time

from django.db.models import Sum, F

from myapp.models import CartItem

logger = logging.getLogger(__name__)


class RequestLogMiddleware:
    """
        Логирование каждого запроса, времени, пользователя
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = round(time.time() - start_time, 3)
        user = request.user if request.user.is_authenticated else 'Аноним'

        logger.info(
            f'{request.method} {request.path} | статус: {response.status_code} | '
            f'пользователь: {user} | {duration}'
        )

        return response


class CartMiddleware:
    """
        Прокидывание корзины юзера во все запросы
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.cart = {
            'items': [],
            'total_qty': 0,
            'total_price': 0,
        }

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)

            totals = cart_items.aggregate(
                total_qty=Sum('quantity'),
                total_price=Sum(F('quantity') * F('product__price')),
            )

            request.cart = {
                'items': cart_items,
                'total_qty': totals['total_qty'] or 0,
                'total_price': totals['total_price'] or 0,
            }

        response = self.get_response(request)
        return response
