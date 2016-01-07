"""
Django settings for Vigtech project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from principal.parameters import *
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l!e-ob)i+sdu2$bq1rbjhvm_3afx8zr6s7_(-ici4r*dtee5)e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []
#cada vez que se acceda se actializa la db de la session
SESSION_SAVE_EVERY_REQUEST=True
# la cerrar el navegador muere la session
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
#    'django_extensions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    #'djcelery',
    'principal',
    #'django_evolution'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Vigtech.urls'

WSGI_APPLICATION = 'Vigtech.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
"""
DATABASES = {
 'default': {
     'ENGINE': 'django.db.backends.postgresql_psycopg2',
     'NAME': 'docker',
     'USER': 'docker',
     'PASSWORD': 'docker',
     'HOST':'localhost',
     'PORT': '49153',
 }
}
"""
DATABASES = {
 'default': {
     'ENGINE': 'django.db.backends.postgresql_psycopg2',
     'NAME': DATABASE,
     'USER': USER,
     'PASSWORD': PASSWORD,
     'HOST' :HOST,
     'PORT': PORT,
 }
}

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,'templates'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static_collected') 

#Cambiar a la ruta del nuevo host
#MEDIA_ROOT="/home/administrador/ManejoVigtech/media/"
#MEDIA_ROOT="/home/japeto/shared/repository/"
MEDIA_ROOT=  REPOSITORY_DIR

#MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
MEDIA_URL = 'media/'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/home/'
#PROYECTOS_DIR="/home/administrador/ManejoVigtech/ArchivosProyectos/" 
