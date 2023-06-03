import datetime
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from portal.models import Category, Subscribers, Post, Author


@shared_task
def previous_week_sending():  # Функция сбора и отправки постов за прошлую неделю подписчикам
    for cat in Category.objects.all():
        subs = [_.user for _ in Subscribers.objects.filter(category=cat)]  # Список пользователей
        week = int(datetime.datetime.today().strftime('%V')) - 1  # Номер прошлой недели. Для проверки можно убрать '- 1'
        posts = Post.objects.filter(post_time__week=week, categories=cat)  # Посты выбранной категории
        if posts:
            for user in subs:
                if user.email:  # Если у подписчика есть почта
                    msg = render_to_string('account/email/new_week_mail.html', context={'user': user.username,
                                                                                        'posts': posts,
                                                                                        'cat': cat.name})
                    message = EmailMessage(  # Сборка сообщения
                        f'Новая выгрузка из Вашей любимой категории: {cat.name}',
                        msg,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[user.email]
                    )
                    message.content_subtype = 'html'  # Указание, что это html сообщение
                    message.send()  #  Отправка


@shared_task
def drop_numbers_of_posts():  # Функция сброса колличества постов в день. Запуск в полночь
    for author in Author.objects.all():
        author.update_numbers_of_posts()
