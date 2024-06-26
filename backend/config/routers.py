from rest_framework.routers import DefaultRouter, SimpleRouter

from config import settings

from request.views import RequestStatsViewSet


if settings.API_DOCS_ENABLE:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("report", RequestStatsViewSet, basename="report")
