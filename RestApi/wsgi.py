"""
WSGI config for RestApi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
print(os.getenv("INT_MYSQL_DB"))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RestApi.settings.local.py')

application = get_wsgi_application()
