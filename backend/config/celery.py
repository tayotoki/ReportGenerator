import os
import re

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery(broker=settings.CELERY_BROKER_URL)
app.config_from_object("django.conf:settings")
app.autodiscover_tasks()


if __name__ == "__main__":
    app.start()
