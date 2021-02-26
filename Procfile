web: gunicorn tracker.wsgi
worker: celery -A tracker worker -l INFO --concurrency 2
beat: celery -A tracker beat