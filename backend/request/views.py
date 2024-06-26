import pandas as pd
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from .filters import RequestFilter
from .models import Request
from .serializers import RequestStatsSerializer
from .paginators import CustomPagination


@extend_schema(tags=["Request"])
class RequestStatsViewSet(ListModelMixin, GenericViewSet):
    serializer_class = RequestStatsSerializer
    filterset_class = RequestFilter
    pagination_class = CustomPagination
    queryset = Request.objects.select_related("state", "status")

    @extend_schema(
        tags=["Request"],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Excel report",
            )
        },
        filters=True,
    )
    @action(detail=False, methods=["GET"])
    def generate_report_by_excel(self, *args, **kwargs):
        """Генерация отчета в виде excel файла"""

        filtered_data = (
            self.filterset_class(
                data=self.request.query_params,
                queryset=self.get_queryset()
            )
            .qs
            .aggregate_stats()
        )

        # TODO: закешировать результаты
        non_filtered_data = self.get_queryset().aggregate_stats()

        columns_for_period = list(filtered_data.values())
        columns_for_all_period = list(non_filtered_data.values())

        data = {
            "Название": [
                "Загруженных заявок",
                "Дубли",
                "На создание",
                "На расширение",
                "Обработка завершена",
                "Возвращена на уточнение",
                "Отправлена в обработку",
                "Пакетов",
                "Пользователей"
            ],
            "За указанный период": columns_for_period,
            "За все время": columns_for_all_period
        }

        df = pd.DataFrame(data)

        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="report.xlsx"'

        with pd.ExcelWriter(response, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Отчет")

        return response
