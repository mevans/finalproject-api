web: gunicorn tracker.wsgi
worker: celery -A tracker worker -l INFO
beat: celery -A tracker beat