import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
