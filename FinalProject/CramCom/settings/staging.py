from .base import *
import os

env = os.environ.get
# SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = 'p9wfrl8=_$8ht(!cm)(x(@9pm(vbhg+$5!9w_1s^g^t(4*22$5'
#os.environ['AWS_ACCESS_KEY_ID'] #os.environ.get('SECRET_KEY')#['SECRET_KEY']

DEBUG = True

DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'
AWS_STORAGE_BUCKET_NAME = env('S3_BUCKET_NAME')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

ADMIN_MEDIA_PREFIX = '/static/admin/'
STATIC_ROOT = 'static'
STATIC_URL = '/static/'

MEDIA_ROOT = path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
#     os.path.join(BASE_DIR, "../../static"),
# ]
#MEDIA_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

#STATIC_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
#del STATIC_ROOT
#del STATICFILES_FINDERS
#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "CramComIntegration",
        'USER': "CCTest",
        'PASSWORD': "nilPax915",
        'HOST': "cramcomintegration.c79ueetdhmiw.us-west-2.rds.amazonaws.com",
        'PORT': 5432,
    }
}

ACCOUNT_EMAIL_REQUIRED = True
# Make email verification mandatory to avoid junk email accounts
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "asgi_redis.RedisChannelLayer",
#         "CONFIG": {
#             'hosts': [('localhost', 6379)],
#         },
#         "ROUTING": "CramCom.routing.channel_routing",
#     },
# }

"""
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
}"""
