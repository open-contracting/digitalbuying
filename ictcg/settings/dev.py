from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ANALYTICS_ID = 'UA-xxxxxx-1'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ml3&38def!wfp=eyu(=71gd(_tlmpujwpb958^7wq)5^=lw5*#'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'localhost:8000'

EMAIL_BACKEND = 'ictcg.email.NotifyEmailBackend'
EMAIL_NOTIFY_API_KEY = os.getenv('EMAIL_NOTIFY_API_KEY', None)
EMAIL_NOTIFY_BASIC_TEMPLATE = "f4ff560b-eec5-4b1c-b6b4-3dc1ed4a1664"

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
