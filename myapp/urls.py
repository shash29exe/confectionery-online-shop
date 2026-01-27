from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('about/', views.about, name='about'),
    path('reviews/', views.reviews, name='reviews'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>', views.remove_from_cart, name='remove_from_cart'),
    path('order/', views.order_view, name='order'),
    path('order/success/<int:order_id>', views.order_success, name='order_success'),
    path('order/<int:order_id>', views.order_detail, name='order_detail'),
    path('order/history', views.order_history, name='order_history'),
]
