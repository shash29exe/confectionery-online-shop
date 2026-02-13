from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from myapp.models import CartItem, Product
from django.http import HttpResponse
from myapp.middleware import CartMiddleware

class CartMiddlewareTests(TestCase):
    """
        Тест корзины анонимного и авторизованного пользователя
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test_user', password='q123456789q')

        self.product = Product.objects.create(name='Торт', price=150)

    def get_response(self, request):
        return HttpResponse('ok')

    def test_anonymous_user_cart(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()

        middleware = CartMiddleware(self.get_response)
        middleware(request)

        self.assertEqual(request.cart['total_qty'], 0)
        self.assertEqual(request.cart['total_price'], 0)
        self.assertFalse(request.cart['has_items'])
        self.assertEqual(request.cart['items'], [])

    def test_authenticated_user_empty_cart(self):
        request = self.factory.get('/')
        request.user = self.user

        middleware = CartMiddleware(self.get_response)
        middleware(request)

        self.assertEqual(request.cart['total_qty'], 0)
        self.assertEqual(request.cart['total_price'], 0)
        self.assertFalse(request.cart['has_items'])