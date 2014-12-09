# django.wsgi is configured to live in projects/django_blank/deploy.

import os
import sys
from os.path import abspath, dirname, join
from site import addsitedir

sys.path.insert(0, abspath(join(dirname(__file__), "../source")))

from django.conf import settings
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from django.core.handlers.wsgi import WSGIHandler
_application = WSGIHandler()
def application(environ, start_response):
  os.environ['AWS_ACCESS_KEY_ID'] = environ['AWS_ACCESS_KEY_ID']
  os.environ['AWS_SECRET_ACCESS_KEY'] = environ['AWS_SECRET_ACCESS_KEY']
  os.environ['DB_PASS'] = environ['DB_PASS']
  os.environ['DJANGO_ENV'] = environ['DJANGO_ENV']
  return _application(environ, start_response)
