import os
import re

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery(broker=settings.CELERY_BROKER_URL)
app.config_from_object("django.conf:settings")
app.autodiscover_tasks()

app.conf.beat_schedule = {

}

app.conf.task_routes = {
    # "common.tasks.send_sms": {"queue": "important"},
    # "analytics.tasks.*": {"queue": "export"},
    # "nats_bus.tasks.*": {"queue": "nats_bus"},
    # "common.tasks.save_remote_image": {"queue": "image"},
    # "common.tasks.convert_to_png": {"queue": "image"},
    # re.compile(r"dynamics\.tasks\.update_layouts_.+"): {"queue": "image"},
    # re.compile(r"dynamics\.tasks\.(?!update_layouts.+).+"): {"queue": "import"},
}

if __name__ == "__main__":
    app.start()
