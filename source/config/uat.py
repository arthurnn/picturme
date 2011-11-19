'''
@author: arthurnn
'''

# Django settings for adidasEcrmLookbook project.
from os.path import abspath, dirname, join

PROJECT_ROOT = abspath(join(dirname(__file__), "../"))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ANALYTICS_ID = 'UA-25908866-2'
RECAPTCHA_PUB_KEY = "6LfA08gSAAAAALDg2e5xIbCujNbNDFD5EATGYGpr"
RECAPTCHA_PRIVATE_KEY = "6LfA08gSAAAAALObXgOJg97Aye6lU93bemuh8lmS"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'adidaslookbook',                      # Or path to database file if using sqlite3.
        'USER': 'adidas',                      # Not used with sqlite3.
        'PASSWORD': 'g2dEyuba',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '127.0.0.1:11211',
#        'VERSION': '1',
#    }
#}

# Keys from user 'django'
AWS_ACCESS_KEY_ID = 'AKIAIC6VFIJCTGUNGU4A'
AWS_SECRET_ACCESS_KEY = '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'

AWS_STORAGE_BUCKET_NAME = 'pictureme_bucket'
AWS_S3_CUSTOM_DOMAIN = 's3.amazonaws.com/pictureme_bucket'
#AWS_S3_CUSTOM_DOMAIN = 'd2579uvf4z4cis.cloudfront.net'
#AWS_CF_DISTRIBUTION_ID = 'E209JJ6DBAW14K'


# There is no MEDIA URL/ROOT or STATIC_ROOT because is using a different Storage
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

STATIC_URL = 'http://%s/static/' % 's3.amazonaws.com/pictureme_bucket'

ADMIN_MEDIA_PREFIX = 'http://%s/admin/' % AWS_S3_CUSTOM_DOMAIN

STATICFILES_DIRS = (
    ("static", "/home/ubuntu/projects/picturme/docroot/static"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        }
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'adidas': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
