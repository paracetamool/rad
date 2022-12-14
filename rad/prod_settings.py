"""
Django settings for rad project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+6lg*ng=b81@%i%n^l8rr-hed_gh1i!zb74_x!q1o+^a-g&5mk'

# SECURITY WARNING: don't run with debug turned on in production!
# TODO: учесть при развертывании

DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'phonenumber_field',
    'colorfield',
    'nested_admin',
    'profiles',
    'app_statistics',
    'Expertize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app_statistics.middleware.MainUserStatisticsMiddleware',
    'profiles.middleware.LastUserActivityMiddleware',
    'profiles.middleware.CurrentUsersStatusMiddleware',
]

ROOT_URLCONF = 'rad.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'statistics_extras': 'app_statistics.templatetags.statistics_extras',
            }
        },
    },
]

# WSGI_APPLICATION = 'rad.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': { 
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             "unix_socket": "/var/lib/mysql/mysql.sock",
#         },
#         'NAME': 'drms_db_prod',
#         'USER': 'drms_db_prod_user',
#         'PASSWORD': 'LZ08/gihd1Y+I+Y',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = '/ex/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240 # higher than the count of fields

# ограничение времени сессии - 8 часов
SESSION_COOKIE_AGE = 28800

GRAPPELLI_ADMIN_TITLE = "Информационная система по выбросам и сбросам"

GRAPPELLI_INDEX_DASHBOARD = 'rad.dashboard.CustomIndexDashboard'

# Список рассылки сообщений об ошибках сервера
ADMINS = (
    ('koltsov', 'koltsov@secnrs.ru'),
    ('lyashko', 'lyashko@secnrs.ru'),
    ('karyakin', 'karyakin@secnrs.ru'),
)
