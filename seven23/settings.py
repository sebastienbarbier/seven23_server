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

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY') or 'k3-=2r(yq-towhfr-$@am&p%ze_&1!m!n7h2p%6*=fn4nr$=d^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') != 'False'

API_VERSION = [1, 0, 0]

# Allow public account creation
ALLOW_ACCOUNT_CREATION = os.environ.get('ALLOW_ACCOUNT_CREATION') == 'True'
SAAS = os.environ.get('SAAS') == 'True'
OLD_PASSWORD_FIELD_ENABLED = True

APPEND_SLASH = False

ALLOWED_HOSTS = ['*']

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
STATIC_ROOT = BASE_DIR + '/collectstatic/'

STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'seven23/static/'),
)

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

LOGIN_URL = '/'

# Database confugration using environment variable DATABASES_URL
DATABASE_URL = os.environ.get('DATABASE_URL') or 'postgres://sbarbier:abcdef@localhost/seven23'
DATABASES = {}
DATABASES['default'] = dj_database_url.parse(DATABASE_URL, conn_max_age=600)

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
    'reset_migrations',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework.authtoken', # Token Authentification
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'rest_auth',
    'seven23.models.accounts',
    'seven23.models.categories',
    'seven23.models.currency',
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

ROOT_URLCONF = 'seven23.urls'

WSGI_APPLICATION = 'seven23.wsgi.application'

CORS_ORIGIN_ALLOW_ALL = True

CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
