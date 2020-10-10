from piclab.settings.base import *

# Override base settings here for dev
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

SECRET_KEY = 'c4#*be@5ud+#5biwv^p6nzp20m=k$@jef4-$q90e!%^qu!sd3n'

# Stop overringing
try:
    from piclab.settings.local import *
except ImportError:
    pass
