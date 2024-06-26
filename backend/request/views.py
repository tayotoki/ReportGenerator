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

    def get_queryset(self):
        queryset = Request.objects.select_related("state", "status")
        match self.action:
            case self.generate_report_by_excel.__name__:
                queryset = (
                    queryset
                    .annotate_count()
                    .annotate_duplicates_count()
                    .annotate_create_state_count()
                    .annotate_expansion_state_count()
                    .annotate_is_finished_count()
                    .annotate_update_info_status_count()
                    .annotate_status_handling_count()
                )
        return queryset

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

        columns = list(filtered_data.values())

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
            "За указанный период": columns,
            "За все время": columns
        }

        df = pd.DataFrame(data)

        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="report.xlsx"'

        with pd.ExcelWriter(response, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Отчет")

        return response
