from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulkymonkey.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

from configurations import importer
importer.install()
app = Celery('bulkymonkey', broker='amqp://guest@localhost//')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend',
)
