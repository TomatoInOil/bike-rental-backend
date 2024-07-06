from .base import *  # noqa

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "general": {
            "format": LOG_FORMAT,
            "datefmt": LOG_DATEFMT,
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "level": "INFO",
            "handlers": [
                "console",
            ],
        },
        "django.db.backends": {
            "level": "DEBUG",
            "handlers": [
                "console",
            ],
            "propagate": False,
        },
    },
}
