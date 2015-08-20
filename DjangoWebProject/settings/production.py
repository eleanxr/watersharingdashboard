from base import *

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('WATERSHARING_DATABASE_NAME', "dbname"),
        'USER': os.environ.get('WATERSHARING_DATABASE_USER', "dbuser"),
        'PASSWORD': os.environ.get("WATERSHARING_DATABASE_PASSWORD", ""),
        'HOST': os.environ.get("WATERSHARING_DATABASE_HOST", "dbhost"),
        'PORT': '',
    }
}

SECRET_KEY = os.environ.get("WATERSHARING_SECRET_KEY", None)
