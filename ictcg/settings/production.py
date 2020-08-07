from .base import *
import dj_database_url
import json
import logging

DEBUG = os.getenv('DJANGO_DEBUG', 'off') == 'on'

ANALYTICS_ID = os.getenv('ANALYTICS_ID', '')

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DATABASES = {}
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*', ]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# Javascript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
LANGUAGE_COOKIE_SECURE = True
LANGUAGE_COOKIE_HTTPONLY = True

try:
    services_json = json.loads(os.getenv('VCAP_SERVICES'))
    aws_s3_config = services_json['aws-s3-bucket'][0]['credentials']

    AWS_STORAGE_BUCKET_NAME = aws_s3_config['bucket_name']
    AWS_ACCESS_KEY_ID = aws_s3_config['aws_access_key_id']
    AWS_SECRET_ACCESS_KEY = aws_s3_config['aws_secret_access_key']
    AWS_S3_REGION_NAME = aws_s3_config["aws_region"]
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME)
    AWS_DEFAULT_ACL = None
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=604800',
    }

    MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

except Exception:
    logging.error('Error configuring S3 media storage')
    pass

try:
    from .local import *
except ImportError:
    pass
