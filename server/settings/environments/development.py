
"""
This file contains all the settings that defines the development server.

SECURITY WARNING: don't run with debug turned on in production!
"""

import logging
from typing import List

from server.settings.components import config
from server.settings.components.common import INSTALLED_APPS, MIDDLEWARE

# Setting the development status:

DEBUG = True

ALLOWED_HOSTS = [
    config('DOMAIN_NAME'),
    'localhost',
    '0.0.0.0',  # noqa: S104
    '127.0.0.1',
    '0.0.0.0:8000',
    '[::1]',
]

CSRF_TRUSTED_ORIGINS = [
    '0.0.0.0:8000'
]


# change to app.example.com in production settings
CORS_ALLOWED_ORIGINS = [
    "http://0.0.0.0:8000",
]


# Installed apps for developement only:

INSTALLED_APPS += (
    'debug_toolbar',
    'nplusone.ext.django',
    'django_migration_linter',
)


# Static files:
# https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-STATICFILES_DIRS

STATICFILES_DIRS: List[str] = []


# Django debug toolbar:
# https://django-debug-toolbar.readthedocs.io

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    # https://github.com/bradmontgomery/django-querycount
    # Prints how many queries were executed, useful for the APIs.
    'querycount.middleware.QueryCountMiddleware',
)


def custom_show_toolbar(request):
    """Only show the debug toolbar to users with the superuser flag."""
    from django.conf import settings
    return request.user.is_superuser and settings.DEBUG


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK':
        'server.settings.environments.development.custom_show_toolbar',
}

# This will make debug toolbar to work with django-csp,
# since `ddt` loads some scripts from `ajax.googleapis.com`:
CSP_SCRIPT_SRC = ("'self'", 'ajax.googleapis.com')
CSP_IMG_SRC = ("'self'", 'data:')
CSP_CONNECT_SRC = ("'self'",)


# nplusone
# https://github.com/jmcarp/nplusone

# Should be the first in line:
MIDDLEWARE = (  # noqa: WPS440
    'nplusone.ext.django.NPlusOneMiddleware',
) + MIDDLEWARE

# Logging N+1 requests:
NPLUSONE_RAISE = True  # comment out if you want to allow N+1 requests
NPLUSONE_LOGGER = logging.getLogger('django')
NPLUSONE_LOG_LEVEL = logging.WARN
NPLUSONE_WHITELIST = [
    {'model': 'admin.*'},
]


# django-test-migrations
# https://github.com/wemake-services/django-test-migrations

# Set of badly named migrations to ignore:
DTM_IGNORED_MIGRATIONS = frozenset((
    ('axes', '*'),
))
