import json
import os
from datetime import timedelta

from google.oauth2 import service_account

from .base_setting import BASE_DIR, SERVER_URL

CATEGORY_IMAGE_DIRECTORY = "category_images"
MOCKUP_DIRECTORY = "mockups"
PRODUCT_PREVIEW_THUMBNAIL_DIRECTORY = "product-list-thumbnail"
PRODUCT_DESIGN_TEMPLATE_DIRECTORY = "product-templates/design-templates"
PRODUCT_PNG_TEMPLATE_DIRECTORY = "png-templates"
PRODUCT_SAMPLE_MOCKUP_DIRECTORY = "product-templates/mockup-samples"
PRODUCT_SIDE_BACKGROUND_DIRECTORY = "3d-transparent-images/previews"
PRODUCT_CUT_IMAGE_DIRECTORY = '3d-transparent-images/originals'
PRODUCT_MODEL_DIRECTORY = 'mockup-generator-models/models'
FRAME_DIRECTORY = "frames"
ARTWORK_DIRECTORY = "artworks"
ARTWORK_DEFAULT_DIRECTORY = "default_artworks"

USE_LOCAL_STORAGE = False
ASSETS_CDN_URL = os.environ.get("ASSETS_CDN_URL")
SAMPLE_MOCKUP_BACKGROUND_DIRECTORY = os.environ.get("SAMPLE_MOCKUP_BACKGROUND_DIRECTORY", None)
USER_PRODUCT_MOCKUP = os.environ.get("USER_MOCKUP_DIRECTORY", None)
USER_FONT = "personalize-fonts"

if os.environ.get("USE_S3") == 'TRUE':
    # aws settings
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
    AWS_DEFAULT_ACL = 'public-read'
    if os.environ.get("AWS_S3_CUSTOM_DOMAIN") is None:
        AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    else:
        AWS_S3_CUSTOM_DOMAIN = os.environ.get("AWS_S3_CUSTOM_DOMAIN")
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_LOCATION = ''
    # s3 static settings
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = 'media/'

elif os.environ.get("USE_GOOGLE_CLOUD_STORAGE") == 'TRUE':
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    STATIC_URL = '/static_files/'
    GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')
    GS_TEMP_BUCKET_NAME = os.environ.get('GS_TEMP_BUCKET_NAME')
    GS_TEMP_UPLOAD_DIR = os.getenv('GS_TEMP_UPLOAD_DIR', 'temp')
    if os.environ.get('GS_CREDENTIALS_FILE_PATH') is not None:
        GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
            os.environ.get('GS_CREDENTIALS_FILE_PATH'))
    elif os.environ.get('GS_CREDENTIALS') is not None:
        GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
            json.loads(os.environ.get('GS_CREDENTIALS')))
    GS_DEFAULT_ACL = 'private'
    GS_EXPIRATION = timedelta(int(os.environ.get('GS_EXPIRATION') or "1209600"))  # default 2 weeks
    MEDIA_URL = 'media/'

    GS_PUBLIC_BUCKET_NAME = os.environ.get('GS_PUBLIC_BUCKET_NAME')
    GS_PUBLIC_CREDENTIALS = service_account.Credentials.from_service_account_info(
        json.loads(os.environ.get('GS_PUBLIC_CREDENTIALS')))
    GS_LOCATION = ''

else:
    USE_LOCAL_STORAGE = True
    GS_CREDENTIALS = service_account.Credentials.from_service_account_info(json.loads(os.environ.get('GS_CREDENTIALS')))
    GS_TEMP_BUCKET_NAME = os.environ.get('GS_TEMP_BUCKET_NAME')
    GS_TEMP_UPLOAD_DIR = os.getenv('GS_TEMP_UPLOAD_DIR', 'temp')
    STATIC_URL = '/static_files/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')
    MEDIA_CONTEXT_PATH = 'media/'
    MEDIA_URL = f'{SERVER_URL}/{MEDIA_CONTEXT_PATH}'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    GS_PUBLIC_BUCKET_NAME = os.environ.get('GS_PUBLIC_BUCKET_NAME')
    GS_PUBLIC_CREDENTIALS = service_account.Credentials.from_service_account_info(
        json.loads(os.environ.get('GS_PUBLIC_CREDENTIALS')))

# STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
