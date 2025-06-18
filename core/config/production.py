import os
from .common import Common


class Production(Common):
    INSTALLED_APPS = Common.INSTALLED_APPS + ('storages', 'gunicorn')

    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
    ALLOWED_HOSTS = ["*"]

    # AWS S3 Storage
    AWS_ACCESS_KEY_ID = os.getenv('DJANGO_AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('DJANGO_AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('DJANGO_AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('DJANGO_AWS_REGION', 'eu-north-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    AWS_QUERYSTRING_AUTH = False
    # AWS_DEFAULT_ACL = "public-read"

    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    # STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'

    AWS_HEADERS = {
        'Cache-Control': 'max-age=86400, s-maxage=86400, must-revalidate',
    }
