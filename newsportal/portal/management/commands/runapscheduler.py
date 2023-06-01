import logging
import datetime
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from portal.models import Author, Subscribers, Post, Category

logger = logging.getLogger(__name__)


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


def drop_numbers_of_posts():  # Функция сброса колличества поство в день. Запуск в полночь
    for author in Author.objects.all():
        author.update_numbers_of_posts()


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            drop_numbers_of_posts,
            trigger=CronTrigger(hour='00', minute='00', second='00'),
            id='drop_numbers_of_posts',
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            previous_week_sending,
            trigger=CronTrigger(day_of_week='mon'),
            id='previous_week_sending',
            max_instances=1,
            replace_existing=True
        )

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")