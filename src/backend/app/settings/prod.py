from .base import *  # noqa

ALLOWED_HOSTS = [
    "backend",
]
CSRF_TRUSTED_ORIGINS = ("http://89.223.123.154", "https://89.223.123.154")

DATABASES = {
    "default": {
        "ENGINE": os.getenv(
            "DB_ENGINE",
            default="django.db.backends.postgresql_psycopg2",
        ),
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

LOG_FILENAME = "backend.log"
LOG_PATH = BASE_DIR.parent / ".data" / "logs"
LOG_PATH.mkdir(parents=True, exist_ok=True)
LOG_PATH = LOG_PATH / LOG_FILENAME
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "general": {
            "format": LOG_FORMAT,
            "datefmt": LOG_DATEFMT,
        },
    },
    "handlers": {
        "file": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_PATH,
            "when": "midnight",
            "interval": 1,
            "backupCount": 14,
            "formatter": "general",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": LOG_LEVEL,
        },
    },
}
