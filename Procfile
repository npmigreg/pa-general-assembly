web: python manage.py collectstatic --no-input; gunicorn pa_analysis.wsgi --log-file - --log-level debug
worker: celery --app pa_analysis.celery.app worker