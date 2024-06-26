import re
from datetime import datetime, timedelta
from typing import TypeVar, Type

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

    UPDATE_FIELDS = [
        "state",
        "coordination",
        "status",
        "finished",
        "handle_time",
    ]

    def cleanup_create_data(self):
        number: str = self.data.get(self.FIELDS_MAPPER["number"]).strip()
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
        author_name: str = self.data.get(self.FIELDS_MAPPER["author"]).strip()
        file_name: str = self.data.get(self.FIELDS_MAPPER["file_name"]).strip()
        created: datetime = datetime.strptime(
            self.data.get(self.FIELDS_MAPPER["created"]),
            "%d.%m.%Y %H:%M:%S"
        )
        finished: datetime = datetime.strptime(
            time,
            "%d.%m.%Y %H:%M:%S"
        ) if (time := self.data.get(self.FIELDS_MAPPER["finished"])) and isinstance(time, str) else None
        handle_time: timedelta = self.cast_to_timedelta(
            self.data.get(self.FIELDS_MAPPER["handle_time"])
        )
        material_full_name: str = self.data.get(self.FIELDS_MAPPER["material_full_name"]).strip()
        technical_documentation: str = self.data.get(self.FIELDS_MAPPER["technical_documentation"])
        batch: str = self.data.get(self.FIELDS_MAPPER["batch"]).strip()
        is_duplicate: bool = self.is_duplicated(
            self.data.get(
                self.FIELDS_MAPPER["state"]
            )
        )

        return {
            key: value
            for key, value in locals().items()
            if key not in ("self", "time")
        }

    def cleanup_update_data(self):
        ...

    def check_fields(self, data: dict) -> bool:
        return True

    @staticmethod
    def is_duplicated(state: str) -> bool:
        return state.strip().startswith("Дубликат")

    @staticmethod
    def handle_statuses(model_: Type[statuses], value: str) -> Type[statuses]:
        """Возвращает объект подходящей модели статуса для заявки"""

        obj, _ = model_._base_manager.get_or_create(name=value) # noqa
        return obj

    @staticmethod
    def cast_to_timedelta(hours: str) -> timedelta:
        handle_time = None

        if hours and re.match(r"\d{1,3}[.]\d{2}", hours):
            hours, partial_hours = map(int, hours.split('.'))
            minutes = (partial_hours * 60) // 100

            handle_time = timedelta(hours=hours, minutes=minutes)
        return handle_time
