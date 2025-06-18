import os
from celery import Celery
from configurations import importer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Local')

importer.install()

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
