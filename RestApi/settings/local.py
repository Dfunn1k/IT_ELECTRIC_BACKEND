from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': getenv("INT_MYSQL_DB"),
        'USER': getenv("INT_MYSQL_USER"),
        'PASSWORD': getenv("INT_MYSQL_PASSWORD"),
        'HOST': getenv("INT_MYSQL_HOST"),
        'PORT': ''
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
