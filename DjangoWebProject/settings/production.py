from base import *

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME', "dbname"),
        'USER': os.environ.get('DATABASE_USER', "dbuser"),
        'PASSWORD': os.environ.get("DATABASE_PASSWORD", ""),
        'HOST': os.environ.get("DATABASE_HOST", "dbhost"),
        'PORT': '',
    }
}

SECRET_KEY = os.environ.get("SECRET_KEY", None)
