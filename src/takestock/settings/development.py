"""
Development settings for takestock.

The development environment is light and local. All data is stored underneath
the development virtualenv.
"""
import os

from takestock.settings.common import *

settings_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.dirname(os.path.dirname(os.path.dirname(settings_path)))
data_path = os.path.join(root_path, 'data')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(data_path, 'takestock.db'),
    }
}

DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(data_path, 'mail')
MEDIA_ROOT = os.path.join(data_path, 'media')
SECRET_KEY = 'abc123'
STATIC_ROOT = os.path.join(data_path, 'static')
TEMPLATE_DEBUG = DEBUG
