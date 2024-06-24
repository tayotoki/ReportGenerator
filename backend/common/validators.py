import re

from django.core.exceptions import ValidationError


def validate_file_extension(value):
    """Название файла имеет тип xlsx."""

    if not re.match(r".*(?:[.]xlsx)$", value):
        raise ValidationError("Неправильный формат. Доступен только xlsx.")
