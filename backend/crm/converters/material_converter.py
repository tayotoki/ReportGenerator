import re
from decimal import Decimal
from typing import Optional

from materials.constants import BasicUnitOfMeasurement

from crm.converters import BaseConverter


class MaterialConverter(BaseConverter):
    FIELDS_MAPPER = {
        "number": "Номер заявки",
        "full_name": "Полное наименование после обработки",
        "code": "Код материала",
        "similar": "Похожие материалы полученные из КП",
        "unit": "БЕИ",
    }

    UPDATE_FIELDS = [
        "full_name",
        "unit",
    ]

    def cleanup_create_data(self):
        number: str = self.data.get(self.FIELDS_MAPPER["number"])
        full_name: str = self.data.get(self.FIELDS_MAPPER["full_name"])
        code: int | None = self.check_code(
            self.data.get(self.FIELDS_MAPPER["code"])
        )
        unit: Optional[BasicUnitOfMeasurement] = this_unit if (
            this_unit := self.data.get(self.FIELDS_MAPPER["unit"])
        ) in BasicUnitOfMeasurement.values else None
        similar = self.parse_material_line(
            line=self.data.get(self.FIELDS_MAPPER["similar"]),
            unit=unit,
        )

        return {
            "number": number,
            "full_name": full_name,
            "code": code,
            "similar": similar,
            "unit": unit,
        }

    def cleanup_update_data(self):
        ...

    @staticmethod
    def check_code(code: str) -> int | None:
        if code.isnumeric():
            code = int(code)
        else:
            code = None
        return code

    @staticmethod
    def check_fields(data: dict) -> bool:
        base_fields = [
            "code",
            "request",  # поле number
        ]
        return bool(data["code"] and data["number"])

    @staticmethod
    def parse_material_line(
            line: str,
            unit: Optional[BasicUnitOfMeasurement] = None
    ) -> list[dict[str, str | Decimal]]:
        if not isinstance(line, (str, bytes)):
            return []

        pattern = (
            r"Номер матераила: (?P<number>\d+)\n"
            r"Точность: (?P<accuracy>[\d.]+)\n"
            r"Полное наименование (?P<full_name>.*)[\n]?"
        )

        matches = re.finditer(pattern, line)
        results = []

        for match in matches:
            results.append({
                "code": match.group("number"),
                "accuracy": Decimal(match.group("accuracy")),
                "full_name": match.group("full_name"),
                "unit": unit,
            })

        return results
