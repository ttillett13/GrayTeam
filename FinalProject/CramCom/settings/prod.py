from .base import *


env = os.environ.get
SECRET_KEY = env('SECRET_KEY')

DEBUG = False

DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'
AWS_STORAGE_BUCKET_NAME = env('S3_BUCKET_NAME')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

MEDIA_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

STATIC_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
del STATIC_ROOT
del STATICFILES_FINDERS
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME': env('PSQL_DB_NAME'),
        'USER': env('PSQL_DB_USER'),
        'PASSWORD': env('PSQL_DB_PASSWD'),
        'HOST': env('PSQL_HOST'),
        'PORT': env('PSQL_PORT'),
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(process)-5d %(thread)d %(name)-50s %(levelname)-8s %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s] %(name)s %(levelname)s %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'syslog': {
         'level': 'ERROR',
         'class': 'logging.handlers.SysLogHandler',
         'facility': 'local7',
         'address': '/dev/log',
         'formatter': 'verbose'
       },
    },
    'loggers': {
        # root logger
        '': {
            'handlers': ['console', 'syslog'],
            'level': 'INFO',
            'disabled': False
        },
        'FinalProject': {
            'handlers': ['console', 'syslog'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# https access only
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True

