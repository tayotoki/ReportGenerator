from django.db.models import TextChoices


class BasicUnitOfMeasurement(TextChoices):
    """Единицы измерения материала"""

    SET = "set", "КОМПЛ"
    PIECE = "piece", "ШТ"
    PACKAGE = "package", "УПАК"
    KILOGRAM = "kilogram", "КГ"
    SQUARE_METR = "square_metr", "М2"
    CBM = "cbm", "М3"
    TN = "tn", "Т"
