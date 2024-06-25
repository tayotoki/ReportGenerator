from django.core.management.base import BaseCommand

from crm.tasks import uploading_data_from_crm


class Command(BaseCommand):
    def handle(self, *args, **options):
        uploading_data_from_crm()
