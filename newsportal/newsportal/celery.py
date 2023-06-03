import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsportal.settings')

app = Celery('newsportal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'previous_week_sending': {
        'task': 'newsportal.tasks.previous_week_sending',
        'schedule': crontab(day_of_week='mon', hour=0, minute=0),
    },
    'drop_numbers_of_posts': {
        'task': 'newsportal.tasks.drop_numbers_of_posts',
        'schedule': crontab(hour=0, minute=0)
    }
}