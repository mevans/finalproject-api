from celery import Celery

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    'variable-notifications': {
        'task': 'core.tasks.send_variable_notifications',
        'schedule': 15,
    }
}

app.autodiscover_tasks()
