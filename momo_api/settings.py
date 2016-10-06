import os
import sys
import datetime

from distutils.util import strtobool


def string_to_bool(bool_as_string):
    """Return a Python bool for a given string"""
    return bool(strtobool(bool_as_string))


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY_CHARACTER_SET = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(0)=+)'
SECRET_KEY = '5*mj(=w3ryh$x8-bulis%g0#*lonkvr1fo@j65gbu!-pm!d=0%'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# https://docs.djangoproject.com/en/1.10/ref/settings/#allowed-hosts
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', ['localhost'])


# https://github.com/ottoyiu/django-cors-headers
CORS_ORIGIN_WHITELIST = (
    'localhost:8080',
    '127.0.0.1:8080',
)


# Authentication Model
# https://docs.djangoproject.com/en/1.10/topics/auth/customizing/#auth-custom-user
AUTH_USER_MODEL = 'account.Account'


# Application definition

# Designate all applications that are enabled in this Django project
# https://docs.djangoproject.com/en/1.10/ref/settings/#installed-apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'rest_framework_swagger',

    'momo_api',
    'momo_api.account',
    'momo_api.base',
    'momo_api.listing',
]


# Middleware hooks into Django's request/response processing
# https://docs.djangoproject.com/en/1.10/topics/http/middleware/
# https://docs.djangoproject.com/en/1.10/ref/settings/#middleware-classes
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # 'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# String representing full Python import path to root URLConf
# https://docs.djangoproject.com/en/1.10/ref/settings/#root-urlconf
ROOT_URLCONF = 'momo_api.urls'


# Python dotted path to the WSGI application used by Django's runserver
WSGI_APPLICATION = 'momo_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Templates
# Used by our browsable api
# https://docs.djangoproject.com/en/1.10/topics/templates/
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

# A string representing the language code for this installation
LANGUAGE_CODE = 'en-us'

# A string representing the time zone for this installation
TIME_ZONE = 'UTC'

# If you set this to False, Django will make some optimizations so as not
# to load the internalization machinery
USE_I18N = True

# If you set this to False, Django will not format dates, numbers, and
# calendars according to the current locale
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# Absolute filesystem path to the directory that will hold static files
STATIC_ROOT = os.environ.get('STATIC_ROOT', '{}/momo_api/static/'.format(BASE_DIR))

# URL that handles the static files served from STATIC_ROOT
STATIC_URL = os.environ.get('STATIC_URL', '/static/')

# Media Files (Pictures, Videos)
# https://docs.djangoproject.com/en/1.10/howto/static-files/#serving-files-uploaded-by-a-user-during-development

# Absolute filesystem path to the directory that will hold user-uploaded files
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', '{}/momo_api/media/'.format(BASE_DIR))

# URL that handles the media served from MEDIA_ROOT
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')

# Upload root for uploading media files
UPLOAD_ROOT = os.environ.get('UPLOAD_ROOT', 'upload/')

# Default file storage class for file-related operations that don't specifiy a specific storage system
# https://docs.djangoproject.com/en/1.10/ref/settings/#default-file-storage
DEFAULT_FILE_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage')


# REST Framework Settings
# http://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'momo_api.base.auth.jwt.JWTAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        # 'momo_api.core.permissions.AllowSafeMethods',
    ),

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
    ),

    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

    'PAGE_SIZE': 50,
}


# Django Rest Framework JWT Library
# https://github.com/GetBlimp/django-rest-framework-jwt

# JWTs are signed with a combination of JWT_MASTER_SECRET_KEY and user.jwt_secret_key
# All tokens will be invalid if this string is changed!
JWT_MASTER_SECRET_KEY = os.environ.get('JWT_MASTER_SECRET_KEY', 'z&B3(s#76qd^-4,C*5vuDk8j8A{:;pCPXDt"7k.@m@"=^Z,Pa*')

# Algorithm used to create the JWT payload
JWT_ALGORITHM = 'HS256'

# The 'JWT' in the header `Authorization: JWT eyJhbGciOiAiSFMyNTYiLCAidHlwIj`
JWT_AUTH_HEADER_PREFIX = 'JWT'

# If you set this to False, JWTs will have no expiration time verification
JWT_VERIFY_EXPIRATION = True

# JWT expiration is half a year
JWT_EXPIRATION_DELTA = datetime.timedelta(weeks=26)

# JWT_LEEWAY allows you to validate an expiration time which is in the past but not very far.
# For example, if you have a JWT payload with an expiration time set to 30 seconds after
# creation but you know that sometimes you will process it after 30 seconds, you can
# set a leeway of 10 seconds in order to have some margin.
# Default is 0 seconds.
JWT_LEEWAY = 0


# If we're in debug mode, enable the browsable API
if 'test' not in sys.argv and DEBUG:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += ('rest_framework.authentication.SessionAuthentication',)
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += ('rest_framework.renderers.BrowsableAPIRenderer',)
