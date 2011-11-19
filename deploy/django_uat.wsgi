# django.wsgi is configured to live in projects/django_blank/deploy.

import os
import sys

from os.path import abspath, dirname, join
from site import addsitedir

sys.path.insert(0, abspath(join(dirname(__file__), "../source")))

os.environ['DJANGO_ENV'] = 'uat'

from django.conf import settings
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()