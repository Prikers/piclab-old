from piclab.google_cloud import get_secret
from piclab.settings.base import *

GS_BUCKET_NAME = 'piclab-tests'
DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY', None)
if SECRET_KEY is None:
    SECRET_KEY = get_secret('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test-db',
    }
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)