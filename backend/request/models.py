from django.db import models

from common.validators import validate_file_extension


class Request(models.Model):
    """Заявка"""

    number = models.CharField(
        verbose_name="Номер заявки",
        max_length=9,
    )
    batch = models.CharField(
        verbose_name="ID пакета",
    )
    state = models.ForeignKey(
        to="RequestState",
        verbose_name="Состояние",
        on_delete=models.SET_NULL,
        related_name="requests",
        null=True,
        blank=True
    )
    status = models.ForeignKey(
        to="RequestStatus",
        verbose_name="Статус",
        on_delete=models.SET_NULL,
        related_name="properties",
        null=True,
        blank=True,
    )
    is_duplicate = models.BooleanField(
        verbose_name="Является дубликатом",
        default=False,
    )
    duplicate = models.ForeignKey(
        to="self",
        verbose_name="Дубликат заявки",
        related_name="duplicates",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    coordination = models.ForeignKey(
        to="RequestCoordination",
        verbose_name="Согласование",
        related_name="requests",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    author_name = models.CharField(
        verbose_name="Автор заявки",
        max_length=255,
    )
    file_name = models.CharField(
        verbose_name="Имя файла",
        max_length=255,
        validators=[validate_file_extension],
    )
    created = models.DateTimeField(
        verbose_name="Время создания",
    )
    finished = models.DateTimeField(
        verbose_name="Время окончания",
        null=True,
        blank=True,
    )
    handle_time = models.DurationField(
        verbose_name="Время от создания до конца обработки",
        null=True,
    )
    material_full_name = models.TextField(
        verbose_name="Полное наименование изначальное",
    )
    technical_documentation = models.CharField(
        verbose_name="НТД",
        max_length=128,
    )

    @property
    def is_handled(self) -> bool:
        return bool(self.finished)

    def __str__(self):
        return f"{self.number}"


class RequestStatuses(models.Model):
    """Различные статусы заявок с текстовым полем"""

    name = models.CharField(
        verbose_name="Название",
        max_length=50,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        abstract = True


class RequestState(RequestStatuses):
    class Meta:
        verbose_name = "Состояние заявки"
        verbose_name_plural = "Состояния заявок"


class RequestCoordination(RequestStatuses):
    class Meta:
        verbose_name = "Согласование заявки"
        verbose_name_plural = "Согласования заявок"


class RequestStatus(RequestStatuses):
    class Meta:
        verbose_name = "Статус заявки"
        verbose_name_plural = "Статусы заявок"
