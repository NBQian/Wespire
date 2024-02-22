import os
from pathlib import Path
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p-ia7h6cdm@1cp#0yaidr#fgha_3$c#7#iaazo9up_t60i$hh$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ['localhost', '127.0.0.1']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	"students",
    "rest_framework",
	"djoser",
    "corsheaders",
	'django_cleanup.apps.CleanupConfig',
	"rest_framework.authtoken",
	"storages"
]

CORS_ORIGIN_ALLOW_ALL = True


MIDDLEWARE = [
	'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'build')],
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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
	os.path.join(BASE_DIR, 'build/static')
]


REST_FRAMEWORK = {
	   'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework.authentication.TokenAuthentication',
	   'rest_framework.authentication.SessionAuthentication',
   ),
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.IsAuthenticated'
    ],
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
	'AUTH_HEADER_TYPES': ('JWT',),
	'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

DJOSER = {
	'LOGIN_FIELD': 'email',
	'USER_CREATE_PASSWORD_RETYPE': True,
	'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
	'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
	'SEND_CONFIRMATION_EMAIL': True,
	'SET_USERNAME_RETYPE': True,
	'SET_PASSWORD_RETYPE': True,
	'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
	'USERNAME_RESET_CONFIRM_URL': 'email/reset/confirm/{uid}/{token}',
	'ACTIVATION_URL': 'activate/{uid}/{token}',
	'SEND_ACTIVATION_EMAIL': True,
	'SERIALIZERS': {
		'user_create': 'students.serializers.UserCreateSerializer',
		'user': 'students.serializers.UserCreateSerializer',
		'user_delete': 'students.serializers.UserDeleteSerializer',
    }
}

AUTH_USER_MODEL = 'students.UserAccount'

# wespireutilities@gmail.com
# qlwc srwy ocbt qmpx
# rono gdwc fzlh zeee

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587 
EMAIL_HOST_USER = 'wespireutilities@gmail.com'
EMAIL_HOST_PASSWORD = "rono gdwc fzlh zeee" 
EMAIL_USE_TLS = True


AWS_ACCESS_KEY_ID = 'AKIAZI2LIVEZ64VSR2V2'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'wespirebackend'
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = 'ap-southeast-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERIFY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

