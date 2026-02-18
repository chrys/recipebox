"""
RecipeBox — Production settings (PostgreSQL + nginx/gunicorn on DigitalOcean VPS).
"""
import os
from .base import *  # noqa: F401,F403

# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------
DEBUG = False

ALLOWED_HOSTS = [
    'www.fasolaki.com',
    'fasolaki.com',
]

CSRF_TRUSTED_ORIGINS = [
    'https://www.fasolaki.com',
    'https://fasolaki.com',
]

SECRET_KEY = os.environ['SECRET_KEY']  # must be set; crash loudly if missing

# ---------------------------------------------------------------------------
# Database — PostgreSQL
# ---------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'recipes'),
        'USER': os.environ.get('DB_USER', 'recipes'),
        'PASSWORD': os.environ['DB_PASSWORD'],  # must be set
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'CONN_MAX_AGE': 60,
    }
}

# ---------------------------------------------------------------------------
# Static & media — served by nginx from /srv/recipes/
# Using /recipes/static/ and /recipes/media/ avoids conflict with other apps
# ---------------------------------------------------------------------------
STATIC_URL = '/recipes/static/'
STATIC_ROOT = '/srv/recipes/staticfiles'

MEDIA_URL = '/recipes/media/'
MEDIA_ROOT = '/srv/recipes/media'

# ---------------------------------------------------------------------------
# Security headers (nginx terminates TLS and forwards via X-Forwarded-Proto)
# ---------------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False  # nginx handles the redirect; avoid double-redirect

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

SECURE_HSTS_SECONDS = 31536000          # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ---------------------------------------------------------------------------
# Logging — stdout/stderr; systemd/journalctl captures it automatically
# ---------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'WARNING'),
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
