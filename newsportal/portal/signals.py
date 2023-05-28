from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from django.core.mail import mail_managers


@receiver(post_save, sender=Post)
def post_notifications(sender, instance, created, **kwargs):
    if created:
        subject = f'Автор {instance.author.user.username} опубликовал новый пост {instance.title}'
    else:
        subject = f'Отредактирован пост: {instance.title}'
    mail_managers(
        subject=subject,
        message=instance.text,
    )
