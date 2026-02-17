from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver
from django.utils import timezone

from myapp.models import Order


@receiver(post_save, sender=User)
def notify_admin_about_new_user(sender, instance, created, **kwargs):
    if created:
        local_time = timezone.localtime(instance.date_joined)
        subject = 'Новая регистрация'
        message = (
            f'Зарегистрирован новый пользователь\n'
            f'Имя: {instance.username}, почта: {instance.email}\n'
            f'Дата регистрации: {local_time.strftime("%Y-%m-%d %H:%M:%S")}'
        )

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL], fail_silently=True)


@receiver(post_save, sender=Order)
def notify_admin_about_new_order(sender, instance, created, **kwargs):
    if created:
        local_time = timezone.localtime(instance.created_at)
        subject = 'Новый заказ'
        message = (
            f'Создан новый заказ!\n'
            f'Номер заказа: {instance.order_number}\n'
            f'ФИО: {instance.name}\n'
            f'Номер телефона: {instance.phone}\n'
            f'Время доставки: {instance.delivery_time or "Не указано"}\n'
            f'Сумма заказа: {instance.total_price} ₽\n'
            f'Дата заказа: {local_time.strftime("%Y-%m-%d %H:%M:%S")}\n'
        )

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL], fail_silently=True)