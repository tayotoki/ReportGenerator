import uuid
from datetime import datetime
from typing import TypeVar, Type
from decimal import Decimal

from request.models import (
    RequestState,
    RequestCoordination,
    RequestStatus,
    RequestStatuses,
)

from crm.converters import BaseConverter


statuses = TypeVar("statuses", bound=RequestStatuses)


class RequestConverter(BaseConverter):
    FIELDS_MAPPER = {
        "number": "Номер заявки",
        "state": "Состояние заявки",
        "coordination": "Согласование",
        "status": "Статус заявки",
        "author": "Автор заявки",
        "file_name": "Имя файла",
        "created": "Дата создания заявки",
        "finished": "Дата окончания обработки",
        "handle_time": "Время от создания заявки до конца обработки (в часах)",
        "material_full_name": "Полное наименование изначальное",
        "technical_documentation": "НТД",
        "batch": "ID пакета"
    }

    def cleanup_create_data(self):
        number: str = self.data.get(self.FIELDS_MAPPER["number"])
        state: Type[statuses] = self.handle_statuses(
            model_=RequestState,
            value=self.data.get(self.FIELDS_MAPPER["state"])
        )
        status: Type[statuses] = self.handle_statuses(
            model_=RequestStatus,
            value=self.data.get(self.FIELDS_MAPPER["status"])
        )
        coordination: Type[statuses] = self.handle_statuses(
            model_=RequestCoordination,
            value=self.data.get(self.FIELDS_MAPPER["coordination"])
        )
        author: str = self.data.get(self.FIELDS_MAPPER["author"])
        file_name: str = self.data.get(self.FIELDS_MAPPER["file_name"])
        created: datetime = datetime.strptime(
            self.data.get(self.FIELDS_MAPPER["created"]),
            "%d.%m.%Y %H:%M:%S"
        )
        finished: datetime = datetime.strptime(
            time,
            "%d.%m.%Y %H:%M:%S"
        ) if (time := self.data.get(self.FIELDS_MAPPER["finished"])) else None
        handle_time: Decimal = Decimal(hours) if (
            hours := self.data.get(self.FIELDS_MAPPER["handle_time"])
        ) else None
        material_full_name: str = self.data.get(self.FIELDS_MAPPER["material_full_name"])
        technical_documentation: str = self.data.get(self.FIELDS_MAPPER["technical_documentation"])
        batch: uuid.uuid4 = uuid.UUID(
            self.data.get(self.FIELDS_MAPPER["batch"])
        ).hex

        return {
            key: value
            for key, value in locals().items()
            if key != "self"
        }

    def cleanup_update_data(self):
        ...

    @staticmethod
    def handle_statuses(model_: Type[statuses], value: str) -> Type[statuses]:
        """Возвращает объект подходящей модели статуса для заявки"""

        obj, _ = model_._base_manager.get_or_create(name=value) # noqa
        return obj
