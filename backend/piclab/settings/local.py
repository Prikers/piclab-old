from piclab.settings.base import *

# Local dev specific settings

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

CORS_ORIGIN_WHITELIST = (
    'http://localhost:8080',
)
CORS_ALLOW_CREDENTIALS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': 'postgres',
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
    }
}

GS_BUCKET_NAME = 'piclab-dev'
