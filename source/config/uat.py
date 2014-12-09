'''
@author: arthurnn
'''

# Django settings for adidasEcrmLookbook project.
from os.path import abspath, dirname, join
import os

PROJECT_ROOT = abspath(join(dirname(__file__), "../"))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'picturme',
        'USER': 'root',
        'PASSWORD': os.getenv('DB_PASS', default=None),
        'HOST': '',
        'PORT': '',
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
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', default=None)

AWS_STORAGE_BUCKET_NAME = 'picturme_bucket'
AWS_S3_CUSTOM_DOMAIN = 's3.amazonaws.com/picturme_bucket'

# There is no MEDIA URL/ROOT or STATIC_ROOT because is using a different Storage
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

STATIC_URL = 'http://%s/static/' % 's3.amazonaws.com/picturme_bucket'

MEDIA_ROOT = '/var/www/picturme/media/'
MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = 'http://%s/admin/' % AWS_S3_CUSTOM_DOMAIN

STATICFILES_DIRS = (
    ("static", "/home/ubuntu/projects/picturme/docroot/static"),
)

PX_CONSUMER_KEY = os.getenv('PX_CONSUMER_KEY', default=None)
