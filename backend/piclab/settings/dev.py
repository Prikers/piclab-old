from piclab.settings.base import *

# --- Override base settings here for dev
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

SECRET_KEY = 'c4#*be@5ud+#5biwv^p6nzp20m=k$@jef4-$q90e!%^qu!sd3n'

# If running on App Engine use Cloud SQL database from within VPC network
# Otherwise database settings will be set from local.py
if os.getenv('GAE_APPLICATION', None):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': '/cloudsql/circular-fusion-290809:europe-west1:piclab',
            'USER': 'postgres',
            'PASSWORD': 'f2aBetvCM7gM192x',
            'NAME': 'piclab-db',
        }
    }

# --- Stop overringing
# Settings will be overwrote by local.py if running on local computer
try:
    from piclab.settings.local import *
except ImportError:
    pass
