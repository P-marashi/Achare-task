from .base import *
from pathlib import Path

# Ensure BASE_DIR is a Path object
BASE_DIR = Path(BASE_DIR)

# Debug should be True in test mode
DEBUG = True

# Allowed hosts for tests
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Database in test environment with Sqlite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',  # Ensure this is a Path object
    },
}

# Use Local-Memory caching for tests to avoid using Redis
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake-test',
    }
}

CACHE_TTL = 60 * 15
