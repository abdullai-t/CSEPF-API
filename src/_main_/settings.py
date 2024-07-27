"""
Django settings for _main_ project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-waq!t5ihsre6s(&-_05+@=o4f^*^w0tb2+n80tybflps4n3adp"

# SECURITY WARNING: don't run with debug turned on in production!
# https://*.massenergize.org, https://*.massenergize.com, https://*.massenergize.dev, https://*.massenergize.test
DEBUG = True
CSRF_TRUSTED_ORIGINS = ["http://*.csepf.test"]

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
	'django_hosts',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'widget_tweaks',
	
	'api',
	'database',
	'admin_site',
]

MIDDLEWARE = [
	'django_hosts.middleware.HostsRequestMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	# 'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.common.CommonMiddleware',
	
	"_main_.utils.middlewares.auth_middleware.AuthMiddleware",
	'django_hosts.middleware.HostsResponseMiddleware',
]

ROOT_URLCONF = '_main_.urls'
ROOT_HOSTCONF = '_main_.hosts'
DEFAULT_HOST = 'default'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = '_main_.wsgi.application'



# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': os.environ.get('DATABASE_ENGINE'),
		'NAME': os.environ.get('DATABASE_NAME'),
		'USER': os.environ.get('DATABASE_USER'),
		'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
		'HOST': os.environ.get('DATABASE_HOST'),
		'PORT': os.environ.get('DATABASE_PORT')
	},
	'test_db': {
		"ENGINE": "django.db.backends.sqlite3",
		"NAME": 'test.sqlite3',
	}
}

#-------- FILE STORAGE CONFIGURATION ---------------------#
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE  = 'storages.backends.s3boto3.S3Boto3Storage'
#-------- FILE STORAGE CONFIGURATION ---------------------#


#-------- AWS CONFIGURATION ---------------------#
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SIGNATURE_VERSION = os.environ.get('AWS_S3_SIGNATURE_VERSION')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False

DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440*3

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
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Simplified static file serving.
STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
