from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Product(models.Model):
    """
        Класс модели продуктов
    """

    name = models.CharField('Название', max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    main_image = models.ImageField('Основное изображение', upload_to='products/', blank=True)
    image = models.ImageField('Изображение', upload_to='products/', blank=True)
    is_available = models.BooleanField('Доступность товара', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.pk])


class ProductImage(models.Model):
    """
        Класс изображения для продуктов
    """

    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')


class Review(models.Model):
    """
        Класс отзывов
    """

    author = models.CharField('Автор', max_length=50)
    text = models.TextField('Содержимое отзыва')
    rating = models.PositiveSmallIntegerField('Оценка', default=5)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_approved = models.BooleanField('Одобрен', default=False)

    def __str__(self):
        return f'Отзыв от {self.author}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']


class CartItem(models.Model):
    """
        Класс корзины
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField('Количество', default=1)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзину'


class Order(models.Model):
    """
        Класс заказов
    """

    STATUS_CHOICES = [
        ('new', 'новый'),
        ('processing', 'в обработке'),
        ('delivered', 'доставлен'),
        ('cancelled', 'отменён')
    ]

    PAYMENT_METHODS = [
        ('cash', 'Наличными при получении'),
        ('card', 'Банковской картой онлайн'),
        ('sbp', 'Система быстрых платежей (СБП)')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Пользователь')
    order_number = models.CharField('Номер заказа', max_length=20, unique=True, default='')
    name = models.CharField('ФИО', max_length=50)
    phone = models.CharField('Номер телефона', max_length=20, unique=True)
    email = models.EmailField('Электронная почта', blank=True)
    address = models.TextField('Адрес доставки', max_length=80)
    delivery_time = models.CharField('Время доставки', max_length=50, blank=True)
    comment = models.TextField('Коментарий к заказу', blank=True)
    created_at = models.DateTimeField('Дата заказа', auto_now_add=True)
    status = models.CharField('Статус заказа', max_length=20, choices=STATUS_CHOICES, default='new')
    payment_method = models.CharField('Метод оплаты', max_length=20, choices=PAYMENT_METHODS, default='cash')
    is_paid = models.BooleanField('Оплачен', default=False)
    total_price = models.DecimalField('Сумма заказа', max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Номер заказа: {self.order_number}'

    def update_total_price(self):
        self.total_price = sum(item.price*item.quantity for item in self.items.all)
        self.save()


class OrderItem(models.Model):
    """
        Класс товара из заказа
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Продукт')
    quantity = models.PositiveIntegerField('Количество', default=1)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.quantity} x {self.product}'
