from base import *

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': os.getenv('WATERDB_NAME'),
        'USER': os.getenv('WATERDB_USER'),
        'PASSWORD': os.getenv('WATERDB_PASSWORD'),
        'HOST': os.getenv('WATERDB_HOST'),
        'PORT': os.getenv('WATERDB_PORT'),
        'OPTIONS': {
            'driver': 'SQL Server Native Client 11.0',
            'MARS_Connection': 'True',
        }
    }
}

SECRET_KEY = "Not really secret!"
