from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .constants import BasicUnitOfMeasurement


class Material(models.Model):
    """Материал для заявки"""

    code = models.PositiveBigIntegerField(
        verbose_name="Код материала",
    )
    full_name = models.TextField(
        verbose_name="Полное наименование",
    )
    unit = models.CharField(
        verbose_name="Единица измерения",
        choices=BasicUnitOfMeasurement.choices,
        max_length=12,
    )

    def __str__(self):
        return f"{self.full_name[:30]}"

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"


class SimilarMaterialToRequest(models.Model):
    """Похожие материалы в заявке"""

    accuracy = models.DecimalField(
        verbose_name="Точность",
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("100.00")),
        ]
    )
    similar = models.ForeignKey(
        to="materials.Material",
        verbose_name="Похожий материал",
        on_delete=models.CASCADE,
    )
    request = models.ForeignKey(
        to="requests.Request",
        verbose_name="Заявка",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Похожий материал"
        verbose_name_plural = "Похожие материалы"
