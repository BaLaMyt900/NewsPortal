from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from portal.models import Category, Subscribers


@shared_task
def mass_mail_send(post):
    """  Рассылка!  """
    list_subs = []  # сборка Емаил адресов подписчиков, если он указан в ЛК
    categories = [_['category__id'] for _ in PostCategory.objects.filter(post=post).values('category__id')]
    categories = Category.objects.filter(id__in=categories)
    for subs in Subscribers.objects.filter(category__in=categories):
        if subs.user.username == post.author.user.username:
            continue  # Пропуск, если пользователь = автор статьи
        if subs.user.email:  # создается отправление если у пользователя введен емаил
            list_subs.append((subs.user.email, subs.user.username, subs.category.name))
    for email, username, cat in list_subs:
        context = {
            'user': username,
            'post': post,
            'cat': cat
        }
        message = EmailMessage(
            f'Вышла новая {"Статья" if post.type == "A" else "Новость"} в Вашей выбранной категории!',
            render_to_string('posts/email/new_post_email.html', context=context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]
        )
        message.content_subtype = 'html'
        message.send()
