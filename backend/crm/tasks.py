from celery import shared_task
from django.conf import settings

from common.decorators import task_logging
from crm.converters.material_converter import MaterialConverter
from crm.converters.request_stats_converter import RequestConverter
from crm.loaders.material_loader import MaterialLoader
from crm.loaders.request_stats_loader import RequestStatsLoader
from crm.services import BaseExcelClient
from materials.models import Material
from request.models import Request


@shared_task
@task_logging
def uploading_data_from_crm() -> str:
    """
    Загрузка данных из CRM
    """

    SHEET_NAME = settings.CRM_SHEET_NAME
    MOCK_CRM_DATA = settings.MOCK_CRM_DATA

    client = BaseExcelClient(MOCK_CRM_DATA, SHEET_NAME)

    loaders = [
        RequestStatsLoader(model=Request, converter=RequestConverter, client=client),
        MaterialLoader(model=Material, converter=MaterialConverter, client=client),
    ]

    updated = 0
    created = 0
    for loader in loaders:
        loader.run()
        created += loader.count_created_objects
        updated += loader.count_updated_objects

    return f"cr={created}, upd={updated}"
