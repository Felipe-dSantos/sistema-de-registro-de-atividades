"""
Django settings for SDRA project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

from django.contrib.messages import constants as messages
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&+llfpu)pz3lbomx@&k_+z&!+94oq1_y)9j51-8+irf-u0pt2p'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

DEBUG = 'RENDER' not in os.environ
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Application definition

INSTALLED_APPS = [
    # "core.apps.CoreConfig",
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'core',
    'crispy_forms',
    'crispy_bootstrap5',
    # 'django_cleanup.apps.CleanupConfig',
    'widget_tweaks',
    'multiupload',
]

#Cripy forms
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'SDRA.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core/templates')],
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

WSGI_APPLICATION = 'SDRA.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

#Local
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'sdra',
#         'USER': 'root',
#         'PASSWORD': 'root',
#         'HOST': 'localhost', # Pode ser 'localhost' se estiver rodando localmente
#         'PORT': '3306', # Normalmente, o MySQL usa a porta 3306
#     }
# }

#produção
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sdra',
        'USER': 'admin',
        'PASSWORD': 'd2K7ROHSV0Qn94scFTH96RspgdrKhDgV',
        'HOST': 'dpg-clnp3ugfvntc73b5hbig-a.oregon-postgres.render.com', # Pode ser 'localhost' se estiver rodando localmente
        'PORT': '5432', # Normalmente, o MySQL usa a porta 3306
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Rio_Branco'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# STATIC_URL = '/static/'

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static")
# ]

# STATIC_ROOT = os.path.join(os.path.dirname(
#     BASE_DIR), "staticfiles")



STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles') 
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Arquivo de Media/upload

# MEDIA_ROOT = '/Arquivos/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# configuraçoes de Autenticação

LOGIN_REDIRECT_URL = 'custom_login_redirect'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

# AUTH_USER_MODEL = 'core.CustomUser'

# settings.py

# Use SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# The host to use for sending email.
EMAIL_HOST = 'smtp.gmail.com'

# Port to use for the SMTP server defined in EMAIL_HOST.
EMAIL_PORT = 587

# Whether to use a TLS (secure) connection when talking to the SMTP server.
EMAIL_USE_TLS = True

# Username to use for the SMTP server defined in EMAIL_HOST.
EMAIL_HOST_USER = 'lds.dossantos1@gmail.com'

# Password to use for the SMTP server defined in EMAIL_HOST.
EMAIL_HOST_PASSWORD = 'panzapmggxiqhwty'

MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warnig',
    messages.ERROR: 'danger'
}

# AUTHENTICATION_BACKENDS = ['core.auth_backends.CPFAuth']



# Formato abreviado para datas (para exibição em locais onde espaço é limitado)
DATE_FORMAT = 'd/m/Y'