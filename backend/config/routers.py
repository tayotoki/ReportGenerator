from rest_framework.routers import DefaultRouter, SimpleRouter

from config import settings


if settings.API_DOCS_ENABLE:
    router = DefaultRouter()
else:
    router = SimpleRouter()
