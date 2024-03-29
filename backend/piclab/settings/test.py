from piclab.google_cloud import get_secret
from piclab.settings.base import *

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_ROOT = './tmp-tests'

DEBUG = False
ALLOWED_HOSTS = ['testserver']

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