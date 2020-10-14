from piclab.settings.base import *
from piclab.storage_backends import get_credentials

# Override base settings here for production
DEBUG = False
ALLOWED_HOSTS = ['*']  # TODO update for production

# SECRET_KEY = os.environ['SECRET_KEY']
SECRET_KEY = 'c4#*be@5ud+#5biwv^p6nzp20m=k$@jef4-$q90e!%^qu!sd3n'  # TODO get from environment variables

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

GS_CREDENTIALS = get_credentials(
    project_id='863654462708',  # TODO os.getenv('GOOGLE_CLOUD_PROJECT')
    secret_id='CREDENTIALS',
    version_id=1,
)
