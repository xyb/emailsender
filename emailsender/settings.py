"""
Django settings for emailsender project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from os import getenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-j=wyi0+-&c$^i_gq*0cuddx88a67q$$h66si^(^0gs1@^5@$mx',
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(getenv('DJANGO_DEBUG', 1)))

if getenv('DJANGO_ALLOWED_HOSTS'):
    ALLOWED_HOSTS = getenv('DJANGO_ALLOWED_HOSTS').split(',')
else:
    ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'mailer',
    'corsheaders',
]

if getenv('EMAIL_BACKEND_TEST'):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = "mailer.backend.DbBackend"
MAILER_EMPTY_QUEUE_SLEEP = 2

EMAIL_USE_SSL = bool(int(getenv('EMAIL_USE_SSL', 0)))
EMAIL_USE_TLS = bool(int(getenv('EMAIL_USE_TLS', 0)))
EMAIL_HOST = getenv('EMAIL_HOST', 'smtp.mydomain.com')
EMAIL_HOST_USER = getenv('EMAIL_HOST_USER', 'xyb@mydomain.com')
EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD', 'password')
EMAIL_PORT = int(getenv('EMAIL_PORT', 465))
EMAIL_FROM = getenv('EMAIL_FROM', 'xyb@mydomain.com')
EMAIL_TIMEOUT = int(getenv('EMAIL_TIMEOUT', 3))

EMAIL_WHITE_LIST = getenv('EMAIL_WHITE_LIST', r'.*')
EMAIL_WHITE_LIST_MESSAGE = getenv('EMAIL_WHITE_LIST_MESSAGE',
                                  'email address not in white list')

if getenv('CORS_ALLOWED_ORIGINS'):
    CORS_ALLOWED_ORIGINS = getenv('CORS_ALLOWED_ORIGINS').split(',')
elif getenv('CORS_ALLOW_ALL_ORIGINS'):
    CORS_ALLOW_ALL_ORIGINS = True

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'emailsender.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'emailsender.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': getenv('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': getenv('DB_USER', 'postgres'),
        'PASSWORD': getenv('DB_PASSWORD', ''),
        'HOST': getenv('DB_HOST', ''),
        'PORT': getenv('DB_PORT', ''),
    }
}
if 'mysql' in DATABASES['default']['ENGINE']:
    DATABASES['default']['OPTIONS'] = {
        # fix mysql error 1452
        "init_command": "SET foreign_key_checks = 0;",
        # fix mysql emoji issue
        'charset': 'utf8mb4',
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
