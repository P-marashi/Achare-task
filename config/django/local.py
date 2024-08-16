from .base import *


# Debug should be True in local mode
DEBUG = env("SETTINGS_DEBUG")


# Allowed hosts
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
# Database in local with Sqlite
DATABASES = {
    "default": env.db(
        "DATABASE_URL", default="mysql://admin:pouya@achare_db:3306/woody"
    ),
}

# Local-Memory caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env("REDIS_URL"),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

CACHE_TTL = 60 * 15
