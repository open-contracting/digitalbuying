"""
WSGI config for ictcg project.

It exposes the WSGI callable as a module-level variable named ``application``.
This is wrapped in the TransLogger which logs requests to the WSGI callable.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
https://docs.pylonsproject.org/projects/waitress/en/stable/logging.html#access-logging
"""
import logging
import sys

from django.core.wsgi import get_wsgi_application
from paste.translogger import TransLogger


handler = logging.StreamHandler(stream=sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(message)s'))

logger = logging.getLogger('wsgi')
logger.addHandler(handler)
logger.propagate = False
logger.setLevel(logging.DEBUG)

application = TransLogger(get_wsgi_application(), logger=logger)
