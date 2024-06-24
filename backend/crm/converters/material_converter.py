import re
from decimal import Decimal
from typing import Optional

from materials.constants import BasicUnitOfMeasurement

from crm.converters import BaseConverter


class RequestConverter(BaseConverter):
    FIELDS_MAPPER = {
        "full_name": "Полное наименование после обработки",
        "code": "Код материала",
        "similar": "Похожие материалы полученные из КП",
        "unit": "БЕИ",
    }

    UPDATE_FIELDS = [
        "full_name",
        "similar",
        "unit",
    ]

    def cleanup_create_data(self):
        material_after_handle: str = self.data.get(self.FIELDS_MAPPER["material_after_handle"])
        code: str = self.data.get(self.FIELDS_MAPPER["code"])
        unit: Optional[BasicUnitOfMeasurement] = this_unit if (
            this_unit := self.data.get(self.FIELDS_MAPPER["unit"])
        ) in BasicUnitOfMeasurement.values else None
        similar = self.parse_material_line(
            line=self.data.get(self.FIELDS_MAPPER["similar"]),
            unit=unit,
        )

        return {
            key: value
            for key, value in locals().items()
            if key != "self"
        }

    def cleanup_update_data(self):
        ...

    @staticmethod
    def parse_material_line(
        line: str,
        unit: Optional[BasicUnitOfMeasurement] = None
    ) -> dict[str, str | Decimal] | None:
        pattern = r"Номер матераила: (?P<number>\d+)\n" \
                  r"Точность: (?P<accuracy>[\d.]+)\n" \
                  r"Полное наименование (?P<full_name>.*)\n"

        match: re.Match = re.search(pattern, line)
        if match:
            return {
                "number": match.group("number"),
                "accuracy": Decimal(match.group("accuracy")),
                "full_name": match.group("full_name"),
                "unit": unit,
            }

        return None
