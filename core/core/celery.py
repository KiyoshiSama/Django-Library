import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-due-books-every-10-seconds': {
        'task': 'transactions.tasks.send_borrow_ending_alert',
        'schedule': crontab(hour=0, minute=0),
    },
}