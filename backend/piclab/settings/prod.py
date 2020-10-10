from piclab.settings.base import *

# Override base settings here for production
DEBUG = False
ALLOWED_HOSTS = ['IP address', 'www.mydomain.com']

SECRET_KEY = os.environ['SECRET_KEY']

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
        'HOST': '/cloudsql/circular-fusion-290809:europe-west1:piclab',
        'USER': 'postgres',
        'PASSWORD': 'f2aBetvCM7gM192x',
        'NAME': 'piclab-db',
    }
}

