# Generated by Django 4.2 on 2024-06-25 15:59

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("request", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Material",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.PositiveBigIntegerField(verbose_name="Код материала")),
                ("full_name", models.TextField(verbose_name="Полное наименование")),
                (
                    "unit",
                    models.CharField(
                        choices=[
                            ("set", "КОМПЛ"),
                            ("piece", "ШТ"),
                            ("package", "УПАК"),
                            ("kilogram", "КГ"),
                            ("square_metr", "М2"),
                            ("cbm", "М3"),
                            ("tn", "Т"),
                        ],
                        max_length=12,
                        null=True,
                        verbose_name="Единица измерения",
                    ),
                ),
            ],
            options={
                "verbose_name": "Материал",
                "verbose_name_plural": "Материалы",
            },
        ),
        migrations.CreateModel(
            name="SimilarMaterialToRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "accuracy",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=5,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.00")),
                            django.core.validators.MaxValueValidator(Decimal("100.00")),
                        ],
                        verbose_name="Точность",
                    ),
                ),
                (
                    "request",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="request.request",
                        verbose_name="Заявка",
                    ),
                ),
                (
                    "similar",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="materials.material",
                        verbose_name="Похожий материал",
                    ),
                ),
            ],
            options={
                "verbose_name": "Похожий материал",
                "verbose_name_plural": "Похожие материалы",
            },
        ),
    ]