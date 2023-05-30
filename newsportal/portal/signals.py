import asyncio
from asgiref.sync import sync_to_async
from django.core.mail import send_mass_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from django.conf import settings


@sync_to_async
def async_send_mail(send_list):
    send_mass_mail(send_list)


@receiver(post_save, sender=Post)
def post_notifications(sender, instance, created, **kwargs):
    if created:
        subject = f'Автор {instance.author.user.username} опубликовал новый пост {instance.title}'
    else:
        subject = f'Автор {instance.author.user.username} отредактировал пост: {instance.title}'
    managers_send_list = []
    for email in settings.MANAGERS:
        managers_send_list.append((
            subject,
            instance.text,
            None,
            [email],
        ))
    asyncio.run(async_send_mail(managers_send_list))
