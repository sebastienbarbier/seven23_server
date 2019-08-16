"""
Django settings for seven23 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

if os.environ.get('SENTRY_DSN'):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[DjangoIntegration()]
    )

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'True'
MAINTENANCE = os.environ.get('MAINTENANCE') == 'True'
API_VERSION = [1, 0, 0]

# Allow public account creation
ALLOW_ACCOUNT_CREATION = os.environ.get('ALLOW_ACCOUNT_CREATION') == 'True'
OLD_PASSWORD_FIELD_ENABLED = True

APPEND_SLASH = True
ALLOWED_HOSTS = ['*']

SAAS = os.environ.get('SAAS') == 'True'
PRICE_YEAR = 45
PRICE_MONTH = 4.5
TRIAL_PERIOD = 30
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: '/home/media/media.lawrence.com/media/'
MEDIA_ROOT = BASE_DIR + '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: 'http://media.lawrence.com/media/', 'http://example.com/media/'
MEDIA_URL = '/_media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' 'static/' subdirectories and in STATICFILES_DIRS.
# Example: '/home/media/media.lawrence.com/static/'

# Static files (CSS, JavaScript, Images)
if os.environ.get('STORAGE') != 'S3':
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'collectstatic')
else:
    # aws settings
    AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL', "https://cellar-c2.services.clever-cloud.com")
    S3_USE_SIGV4 = False
    AWS_S3_SIGNATURE_VERSION = "s3"
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN')
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=0'}
    AWS_S3_FILE_OVERWRITE = True
    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATIC_ROOT = os.path.join(BASE_DIR, 'collectstatic')

STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'seven23/static'),
)


LOGIN_URL = '/'

# Database confugration using environment variable DATABASES_URL
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASES = {}
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL, conn_max_age=600)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]


TEMPLATES = [
    {
        'BACKEND':
            'django.template.backends.django.DjangoTemplates'
        ,
        'DIRS': [
            BASE_DIR + '/seven23/templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
            ]
        }
    },
]

# Application definition
INSTALLED_APPS = (
    'mptt',
    'colorfield',
    'sass_processor',
    'reset_migrations',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken', # Token Authentification
    'drf_yasg',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth.registration',
    'rest_auth',
    'storages',
    'seven23.models.accounts',
    'seven23.models.categories',
    'seven23.models.currency',
    'seven23.models.events',
    'seven23.models.goals',
    'seven23.models.profile',
    'seven23.models.stats',
    'seven23.models.saas',
    'seven23.models.terms',
    'seven23.models.tokens',
    'seven23.models.transactions'
)

SITE_ID = 1 # Required by rest_auth

MIDDLEWARE = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'seven23.middleware.maintenance_middleware',
    'seven23.models.stats.middleware.active_user_middleware',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
}

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'seven23.models.rest_auth.serializers.UserSerializer',
    'PASSWORD_RESET_SERIALIZER': 'seven23.models.rest_auth.serializers.PasswordResetSerializer',
}

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}

LOGIN_URL = '/admin/'

ROOT_URLCONF = 'seven23.urls'

WSGI_APPLICATION = 'seven23.wsgi.application'

CORS_ORIGIN_ALLOW_ALL = True

CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL')
DEFAULT_FROM_EMAIL = CONTACT_EMAIL


if os.environ.get('EMAIL_BACKEND_CONSOLE') == 'True':
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
