from .base import *  # noqa: F403
from .base import env

# configure db name for testing
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="postgres://djangouser:djangopw@db:5432/djangodb_test",
    ),
}

DJANGO_VITE = {
    "default": {
        "dev_mode": env.bool("DJANGO_VITE_DEV_MODE", default=False),
        "dev_server_port": env("DJANGO_VITE_DEV_SERVER_PORT", default="5173"),
    }
}