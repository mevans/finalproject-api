import os

from celery import Celery

settings_module = "tracker.production" if 'PRODUCTION' in os.environ else 'tracker.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    'variable-notifications': {
        'task': 'core.tasks.send_variable_notifications',
        'schedule': 15,
    }
}

app.autodiscover_tasks()
