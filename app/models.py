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
        return reverse('product-detail', args=[self.pk])


class ProductImage(models.Model):
    """
        Класс изображения для продуктов
    """

    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')