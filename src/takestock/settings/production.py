"""
Production settings for takestock.

Because it's a bad idea to keep production credentials in version control,
certain required settings are omitted here. The omitted settings are expected
to be in a settings file that lives only on the production server, with
appropriate protections in terms of location and permissions.

To pull in those settings, set the environment variable TAKESTOCK_CONFIG_PATH
to the absolute path of the file before running takestock code.

The omitted settings that are expected to be in the server-only file are::

    DATABASES['default']['PASSWORD'] = 'db-password'
    EMAIL_HOST_PASSWORD = 'email-password'
    SECRET_KEY = 'some-long-and-very-random-string'

"""
import os

from takestock.settings.common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'takestock',
        'USER': 'takestock',
        'HOST': 'localhost',
    }
}
DEBUG = False
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'jbierfeldt@gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
MEDIA_ROOT = '/webapps/takestock/media/'
STATIC_ROOT = '/webapps/takestock/static/'
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    '.who-got.in', # Allow domain and subdomains
    '.who-got.in.', # Also allow FQDN and subdomains
	]

if 'TAKESTOCK_CONFIG_PATH' in os.environ:
    execfile(os.environ['TAKESTOCK_CONFIG_PATH'])
