from .base import *


# Debug should be False in production mode
DEBUG = env("SETTINGS_DEBUG")


# Allowed hosts (Set your domain here)
ALLOWED_HOSTS = [DOMAIN_NAME, f"www.{DOMAIN_NAME}"]


DATABASES = {
    "default": env.db(
        "DATABASE_URL", default="postgres://admin:pouya@achare-database:5432/achare"
    ),
}


# Caching with redis
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env("REDIS_URL"),
    }
}

CACHE_TTL = 60 * 15
