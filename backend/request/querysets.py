from django.db.models import QuerySet, Count, Case, When, IntegerField, Q, Sum, F, Subquery, Value


class RequestQuerySet(QuerySet):
    def aggregate_stats(self):
        """Полная статистика по заявкам"""

        return self.aggregate(
            total_count=Count("id"),
            total_duplicates_count=Count(
                "id",
                filter=Q(is_duplicate=True),
            ),
            total_create_state_count=Count(
                "id",
                filter=Q(state__name__icontains="добавление")
            ),
            total_expansion_state_count=Count(
                "id",
                filter=Q(state__name__icontains="расширение")
            ),
            total_finished_count=Count(
                "id",
                filter=Q(finished__isnull=False)
            ),
            total_update_info_status_count=Count(
                "id",
                filter=Q(status__name__iexact="возвращена на уточнение")
            ),
            total_status_handling_count=Count(
                "id",
                filter=Q(status__name__iexact="отправлена в обработку")
            ),
            total_batch_count=Count("batch", distinct=True),
            total_users_count=Count("author_name", distinct=True),
        )
