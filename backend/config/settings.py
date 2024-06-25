from os import environ, getenv
from os.path import join
from pathlib import Path
from sys import argv

from django.utils.translation import gettext_lazy as _

SITE_HOST = getenv("SITE_HOST")

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = getenv("SECRET_KEY")

TESTING = "test" in argv or any("pytest" in arg for arg in argv)
DEBUG = getenv("DEBUG", "True") == "True" and not TESTING
API_DOCS_ENABLE = getenv("API_DOCS_ENABLE", "True") == "True"

CRM_SHEET_NAME = "Data"
MOCK_CRM_DATA = BASE_DIR / "crm" / "mock_data" / "testing_data.xlsx"

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ["http://localhost", "http://localhost:3000"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # app
    "crm.apps.CrmConfig",
    "materials.apps.MaterialsConfig",
    "users.apps.UsersConfig",
    "request.apps.RequestConfig",
    # third-party
    "django_filters",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

    def show_toolbar_callback(_):
        return DEBUG

    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": "config.settings.show_toolbar_callback"}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("POSTGRES_NAME"),
        "USER": getenv("POSTGRES_USER"),
        "PASSWORD": getenv("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": getenv("POSTGRES_PORT"),
        "CONN_MAX_AGE": 600,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

USE_TZ = True
USE_L10N = True
USE_I18N = True
LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Moscow"
LANGUAGES = (("ru", _("Russian")), ("en", _("English")))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/s/"
STATIC_ROOT = join(BASE_DIR, "static")

# Media
MEDIA_URL = "/m/"
MEDIA_ROOT = join(BASE_DIR, "media")
if TESTING:
    DEFAULT_FILE_STORAGE = "django_hashedfilenamestorage.storage.HashedFilenameFileSystemStorage"
    BASE_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
else:
    DEFAULT_FILE_STORAGE = "common.storages.HashedFilenameS3Boto3Storage"
    BASE_FILE_STORAGE = "common.storages.CustomS3Boto3Storage"

FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
FILE_UPLOAD_PERMISSIONS = 0o644

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": ["drf_orjson_renderer.renderers.ORJSONRenderer"],
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.SessionAuthentication"],
}
if not API_DOCS_ENABLE:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
        "rest_framework.renderers.JSONRenderer"
    ]

# logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "rabbitmq": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "rabbitmq"},
    },
    "loggers": {"": {"level": "INFO", "handlers": ["console"]}},
}

CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TIMEZONE = "Europe/Moscow"
CELERY_RESULT_SERIALIZER = "json"
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"

if "SENTRY_DSN" in environ:
    import sentry_sdk
    # from sentry_sdk.integrations.celery import CeleryIntegration
    # from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=environ["SENTRY_DSN"],
        # integrations=[DjangoIntegration(), CeleryIntegration()],
    )

if not TESTING:
    CACHES = {
        "default": {"BACKEND": "redis_cache.RedisCache", "LOCATION": "redis:6379"},
    }

SESSION_COOKIE_AGE = 31_536_000
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.SessionAuthentication"],
}

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]
if not DEBUG or not API_DOCS_ENABLE:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ["rest_framework.renderers.JSONRenderer"]

# Imagekit
IMAGEKIT_CACHEFILE_DIR = "c"
IMAGEKIT_DEFAULT_FILE_STORAGE = BASE_FILE_STORAGE
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = "imagekit.cachefiles.strategies.Optimistic"

# Кастомный пользователь
AUTH_USER_MODEL = "users.User"
# Сайт
SITE_ID = 1
