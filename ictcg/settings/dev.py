from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DJANGO_DEBUG = True

ANALYTICS_ID = 'UA-xxxxxx-1'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ml3&38def!wfp=eyu(=71gd(_tlmpujwpb958^7wq)5^=lw5*#'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gdmp-ictcg-dev',
    }
}

INSTALLED_APPS += [
    'debug_toolbar'
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

INTERNAL_IPS = [
    '127.0.0.1'
]
try:
    from .local import *
except ImportError:
    pass
