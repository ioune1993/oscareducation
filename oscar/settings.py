"""
Django settings for oscar project.
For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*zz(eb9rfi-m)ke!*zsii9t3+xh5dpvf8p0gyj=i0ul5pw9$)!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DEBUG_PROPAGATE_EXCEPTIONS = False


ALLOWED_HOSTS = []

LOGIN_REDIRECT_URL = "/"


# Application definition

try:
    from additional_apps import ADDITIONAL_APPS
except ImportError:
    ADDITIONAL_APPS = ()


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentification',
    'bootstrap3',
    'django_extensions',
    'debug_toolbar',
    'django_pdb',
    'crispy_forms',
    'oscar',  # hack: add self for templates dir
    'promotions',
    'skills',
    'planification',
    'examinations',
    'student',
    'stats',
    'compressor',
    'users',
    'resources',
    'end_test_poll',

) + ADDITIONAL_APPS

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_pdb.middleware.PdbMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [os.path.join(BASE_DIR, "templates")],
    "OPTIONS": {
        "debug": DEBUG,
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'django.template.context_processors.media',
        ],
        "loaders": (
            'hamlpy.template.loaders.HamlPyFilesystemLoader',
            'hamlpy.template.loaders.HamlPyAppDirectoriesLoader',
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
    },
}]

ROOT_URLCONF = 'oscar.urls'

WSGI_APPLICATION = 'oscar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'oscar',
        'USER': 'oscar',
        'PASSWORD': 'oscar',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# https://docs.djangoproject.com/en/1.10/topics/logging/

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'fr-be'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CRISPY_TEMPLATE_PACK = 'bootstrap3'

BOOTSTRAP3 = {
    "css_url": "/static/css/bootstrap.min.css",
}

try:
    from settings_local import *
except ImportError:
    pass

if "STATIC_ROOT" not in globals():
    COMPRESS_ROOT = os.path.join(BASE_DIR, "static_compressed")

CRISPY_FAIL_SILENTLY = not DEBUG

INTERNAL_IPS = ('127.0.0.1',)

# Email settings
#DEFAULT_FROM_EMAIL = 'noreply@louvainfo.be'
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Host for sending e-mail.
EMAIL_HOST = 'smtp.gmail.com'

# Port for sending e-mail.
EMAIL_PORT = 587

# Credentials to account
# You need to "allow less scure apps" on your Gmail account first
EMAIL_HOST_USER ="euredukaoscar.noreply@gmail.com"
EMAIL_HOST_PASSWORD ="7A=em=nBt@+r3MFq"

EMAIL_USE_TLS = True