import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tracker.settings")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    'every-15-seconds': {
        'task': 'patient.tasks.send_email',
        'schedule': 15,
    }
}

app.autodiscover_tasks()
