"""
Django settings for base project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5$p4*o@vsygv*ide!@ay@-(54zro=z%g(9@exm)9vuc5gdp_&9'

# API_KEY
API_KEY = '5p3whPvbCHDqKRqxLKhzLOU2dT9B2Z'

DJ_SECRET_KEY = 'OsuMhWY/TkZDRJQ2KBIUEtI6dx+RevllbckPYyez1qw'
DJ_PUBLIC_KEY = 'DO00ELXFPFGXPC7PURUP'
DJ_BUCKET_NAME = 'bucket'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'Admin.apps.AdminConfig',
    'rest_framework',
    'widget_tweaks',
    'allauth',
    'allauth.account',
    'corsheaders'
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'templates', 'allauth')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'custom_templatetag': 'Admin.templatetags.exstra_fields',

            }
        },
    },
]

WSGI_APPLICATION = 'base.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    # railway postgress database
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'railway',
    #     'USER': 'postgres',
    #     'PASSWORD': 'dgvZyDpofiQBMIFLjBUh',
    #     'HOST': 'containers-us-west-189.railway.app',
    #     'PORT': '6461',
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'apps',
        'USERNAME': 'apps',
        'PASSWORD': 'omar191513',
        'HOST': 'dg-3.c70ljiexmnqa.us-east-2.rds.amazonaws.com',
        'PORT': '5432',
    }
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

STATIC_URL = '/static/'
MEDIA_URL = '/img/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# static

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'base/static/')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/img')


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',

    'allauth.account.auth_backends.AuthenticationBackend',
]


CORS_ALLOW_ALL_ORIGINS = True

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = False

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = '/login/'


if os.getcwd() == '/app':
    DEBUG = False
