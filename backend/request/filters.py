from django_filters import DateTimeFilter, FilterSet

from .models import Request


class RequestFilter(FilterSet):
    start_date = DateTimeFilter(field_name="created", lookup_expr="gte")
    end_date = DateTimeFilter(field_name="created", lookup_expr="lte")

    class Meta:
        model = Request
        fields = ("start_date", "end_date")
