# Configurações do Django para o projeto SDRA

Este arquivo contém as configurações principais do projeto Django SDRA. Para mais informações sobre as configurações, consulte [a documentação oficial do Django](https://docs.djangoproject.com/en/4.2/topics/settings/) e [a referência de configurações](https://docs.djangoproject.com/en/4.2/ref/settings/).

## Configurações Gerais

```python
from pathlib import Path
import os

## Build paths inside the project like this: BASE_DIR / 'subdir'.
`BASE_DIR = Path(__file__).resolve().parent.parent`

##  SECURITY WARNING: keep the secret key used in production secret!
`SECRET_KEY = 'django-insecure-&+llfpu)pz3lbomx@&k_+z&!+94oq1_y)9j51-8+irf-u0pt2p'`

## SECURITY WARNING: don't run with debug turned on in production!
`DEBUG = 'RENDER' not in os.environ`
`ALLOWED_HOSTS = ['*']`

`EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"`

```
## Aplicações Instaladas
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'core',
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
    'multiupload',
]


```
## Configurações do Cripy Forms
```
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

```
## Middleware
```
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

```
## Configurações de Templates
```
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

```
## Configurações do Banco de Dados
```
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

```
## Internacionalização
```
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Rio_Branco'
USE_I18N = True
USE_TZ = True

```
## Configurações de Arquivos estáticos e de Mídia
```
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

```
## Configurações de Email
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'lds.dossantos1@gmail.com'
EMAIL_HOST_PASSWORD = 'panzapmggxiqhwty'

```
## Configurações de Mensagens
```
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warnig',
    messages.ERROR: 'danger'
}

```
## Configurações de Autenticação
```
AUTH_USER_MODEL = 'core.CustomUsuario'
LOGIN_REDIRECT_URL = 'custom_login_redirect'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

```
## Outras Configurações
```
# Formato abreviado para datas (para exibição em locais onde espaço é limitado)
DATE_FORMAT = 'd/m/Y'


```