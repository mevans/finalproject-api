"""
Django settings for tracker project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&z5swzqxt32f@an*a$(9ax431cwo0fefdv7@g7r9-$1&u6ad9n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',
    'doctor',
    'patient',

    'rest_framework',
    'rest_framework.authtoken',

    'dj_rest_auth',

    'corsheaders',
    'fcm_django',

    'django_celery_beat',
    'recurrence',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ]
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.FcmTokenMiddleware'
]

ROOT_URLCONF = 'tracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'tracker.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "d6o64nasf361ad",
        'HOST': "ec2-54-74-156-137.eu-west-1.compute.amazonaws.com",
        'USER': "fgcnxbiqxeybhw",
        'PASSWORD': "61ad9e6fca95ebf0ea44d8e2618502106050ea4d7393afe8f6aee988a8fab5bd",
        'PORT': '5432'
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'core.User'
REST_USE_JWT = True

SITE_ID = 1

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=365),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365)
}

REST_AUTH_SERIALIZERS = {
    'JWT_SERIALIZER': 'core.serializers.JWTSerializer'
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

CORS_ORIGIN_ALLOW_ALL = True

FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "AAAA_alpeRc:APA91bHfjajO0isrq6PNw75dwneWxfXYPIBRi7a7bY0j9138BJRomd-x5H6wm9UNVAr4xoN76kQ1UOUu0ZPHuzPx6J7Y4IfzYeDi-7rq0ulP2XNNQYhnZCIm3bKc_2GYN3k55Z04p0eU",
    "ONE_DEVICE_PER_USER": True,
    "DELETE_INACTIVE_DEVICES": True,
}

FIREBASE_API_KEY = "AIzaSyAyK9FTj-eT7LS8ZXRJ-up2NaXruighOLQ"

ANDROID_PACKAGE_NAME = "uk.co.evans99.matthew.app"
IOS_BUNDLE_ID = "uk.co.evans99.matthew.app"

EMAIL_ = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "auth.smtp.1and1.co.uk"
EMAIL_PORT = 25
EMAIL_HOST_USER = "matthew@evans99.co.uk"
EMAIL_HOST_PASSWORD = "ishbel2002"
EMAIL_USE_TLS = True

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER",
                                   "redis://:pb566d0c906ff52fa7eebb7656c6151cc5536eabaa955500a823cefd61f7fa5d1@ec2-34-241-222-85.eu-west-1.compute.amazonaws.com:12479")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND",
                                       "redis://:pb566d0c906ff52fa7eebb7656c6151cc5536eabaa955500a823cefd61f7fa5d1@ec2-34-241-222-85.eu-west-1.compute.amazonaws.com:12479")
