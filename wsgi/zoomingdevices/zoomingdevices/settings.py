"""
Django settings for zoomingdevices project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from . import keys

# a setting to determine whether we are running on OpenShift
ON_OPENSHIFT = False
if 'OPENSHIFT_REPO_DIR' in os.environ:
    ON_OPENSHIFT = True
# if 'OPENSHIFT_APP_NAME' in os.environ:
#     DB_NAME = os.environ['OPENSHIFT_APP_NAME']
# if 'OPENSHIFT_DB_USERNAME' in os.environ:
#     DB_USER = os.environ['OPENSHIFT_DB_USERNAME']
# if 'OPENSHIFT_DB_PASSWORD' in os.environ:
#     DB_PASSWD = os.environ['OPENSHIFT_DB_PASSWORD']
# if 'OPENSHIFT_DB_HOST' in os.environ:
#     DB_HOST = os.environ['OPENSHIFT_DB_HOST']
# if 'OPENSHIFT_DB_PORT' in os.environ:
#     DB_PORT = os.environ['OPENSHIFT_DB_PORT']

# from zoomingdevices import keys
DJ_PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(DJ_PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = keys.SECRET_KEY
# SECRET_KEY = '!iudke*hi8vo#qyntq5yxm+p2itkuqg-m@bo8o%+cbnq(h%@@-'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',
    'debug_toolbar',
)

INSTALLED_APPS += (
    'devices',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ('127.0.0.1', keys.MY_IP)

SHOW_TOOLBAR_CALLBACK = lambda x: True    # force show debug toolbar

ROOT_URLCONF = 'zoomingdevices.urls'

WSGI_APPLICATION = 'zoomingdevices.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if ON_OPENSHIFT:
    # os.environ['OPENSHIFT_DB_*'] variables can be used with databases created
    # with rhc app cartridge add (see /README in this git repo)
    DATABASES = {
        'default': {
            'ENGINE': keys.OS_DB_BACKEND,
            'NAME': keys.OS_DB_NAME,
            'USER': keys.OS_DB_USER,
            'PASSWORD': keys.OS_DB_PASSWORD,
            'HOST': keys.OS_DB_HOST,
            'PORT': keys.OS_DB_PORT,
        }
    }
    CACHES = {
        "default": {
            "BACKEND": keys.OS_CACHE_BACKEND,
            "LOCATION": keys.OS_CACHE_LOCATION,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/0",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = False

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')

########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
            'rest_framework.filters.DjangoFilterBackend',
            'rest_framework.filters.SearchFilter',),

    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/min',
        'user': '100/min'
    }
}
