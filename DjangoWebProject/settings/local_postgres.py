from base import *

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'watersharingdb',
        'USER': 'watersharinguser',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

SECRET_KEY = "Not really secret!"

MEDIA_URL = "http://localhost:8001/"
