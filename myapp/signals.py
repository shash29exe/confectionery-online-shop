from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver


@receiver(post_save, sender=User)
def notify_admin_about_new_user(sender, instance, created, **kwargs):
    if created:
        subject = 'Новая регистрация'
        message = (
            f'Зарегистрирован новый пользователь\n'
            f'Имя: {instance.username}, почта: {instance.email}'
        )

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL], fail_silently=True)