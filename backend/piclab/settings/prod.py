from piclab.settings.base import *
from piclab.google_cloud import get_credentials, get_secret

# Override base settings here for production
DEBUG = False
ALLOWED_HOSTS = [GOOGLE_CLOUD_HOST]
CORS_ORIGIN_WHITELIST = (
    f'https://{GOOGLE_CLOUD_HOST}',
)
CORS_ALLOW_CREDENTIALS = True

SECRET_KEY = get_secret('SECRET_KEY')

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': f'/cloudsql/{GOOGLE_CLOUD_PROJECT}:{GOOGLE_CLOUD_REGION}:{get_secret("DATABASE_HOST")}',
        'USER': 'postgres',
        'PASSWORD': get_secret('DATABASE_PASSWORD'),
        'NAME': get_secret('DATABASE_NAME'),
    }
}

GS_CREDENTIALS = get_credentials('CREDENTIALS')
