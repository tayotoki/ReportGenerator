from django_filters import DateTimeFromToRangeFilter, FilterSet

from .models import Request


class RequestFilter(FilterSet):
    created_range_filter = DateTimeFromToRangeFilter(field_name="created", label="Фильтр по периоду создания заявок")

    class Meta:
        model = Request
        fields = ()
