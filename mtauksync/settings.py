from os import environ
from pathlib import Path

from django.urls import reverse_lazy


def get_env(key, default=None):
    val = environ.get(key, default)
    if val == 'True':
        val = True
    elif val == 'False':
        val = False
    return val


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = get_env(
    'SECRET_KEY', '%c$7zt6go=)ockyzvu07-zjoxa&ynd$xlllh-815n3&fm#%03e')

DEBUG = get_env('DEBUG', True)

ALLOWED_HOSTS = ['*']

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'drf_yasg',
    'django_q',
]

LOCAL_APPS = [
    'user_profile.apps.UserProfileConfig',
    'mt_client',
    'initcmds',
    'auk_client'
]

if DEBUG:
    # Silk
    THIRD_PARTY_APPS = ['silk', ] + THIRD_PARTY_APPS

    SILKY_PYTHON_PROFILER = True
    SILKY_PYTHON_PROFILER_BINARY = True
    SILKY_PYTHON_PROFILER_RESULT_PATH = Path.joinpath(BASE_DIR, 'silk')
    SILKY_MAX_REQUEST_BODY_SIZE = -1  # Silk takes anything <0 as no limit
    SILKY_MAX_RESPONSE_BODY_SIZE = -1
    SILKY_META = True

    # drf-generators
    THIRD_PARTY_APPS = THIRD_PARTY_APPS + ['drf_generators', ]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE = ['silk.middleware.SilkyMiddleware', ] + MIDDLEWARE

ROOT_URLCONF = 'mtauksync.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path.joinpath(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'mtauksync.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env('POSTGRES_DB', 'postgres_db'),
        'USER': get_env('POSTGRES_USER', 'postgresuser'),
        'PASSWORD': get_env('POSTGRES_PASSWORD', 'mysecretpass'),
        'HOST': get_env('POSTGRES_HOST', 'localhost'),
        'PORT': 5432
    },
    'mtdb': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env('MT_MYSQL_DB', 'mt_db'),
        'USER': get_env('MT_MYSQL_USER', 'mtuser'),
        'PASSWORD': get_env('MT_MYSQL_PASSWORD', 'mtpass'),
        'HOST': get_env('MT_MYSQL_HOST', 'localhost'),
        'PORT': 3306,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

AUTH_PASSWORD_VALIDATORS = []

AUTH_USER_MODEL = 'user_profile.UserProfile'

LANGUAGE_CODE = get_env('LANGUAGE_CODE', 'en-us')

TIME_ZONE = get_env('TIME_ZONE', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = Path.joinpath(BASE_DIR, 'static')
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'DEFAULT_AUTO_SCHEMA_CLASS': 'drf_yasg.inspectors.SwaggerAutoSchema',
    'VALIDATOR_URL': None,
    'DEEP_LINKING': True,
    'USE_SESSION_AUTH': True,
}

LOGIN_URL = reverse_lazy('admin:login')
LOGOUT_URL = reverse_lazy('admin:logout')

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
            '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': get_env('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}

Q_CLUSTER = {
    'name': 'DjangORM',
    'workers': 2,
    'retry': 360,
    'timeout': 300,
    'queue_limit': 50,
    'bulk': 10,
    'ack_failures': True,
    'orm': 'default'
}

AUK_TOKEN = get_env('AUK_TOKEN', "testtoken")

AUK_PLATFORM_PERIOD = get_env('AUK_PLATFORM_PERIOD', 5)
AUK_CONTAINER_PERIOD = get_env('AUK_CONTAINER_PERIOD', 5)
MT_PERIOD = get_env('MT_PERIOD', 3)


FIRST_RUN_DAYS = get_env('FIRST_RUN_DAYS', 30)

ENABLE_MT_SYNC = get_env('ENABLE_MT_SYNC', False)
