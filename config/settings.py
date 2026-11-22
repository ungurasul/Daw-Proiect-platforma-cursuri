from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

if not os.environ.get('DJANGO_SECRET_KEY'):
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        for line in env_file.read_text(encoding='utf-8').splitlines():
            if line.startswith('DJANGO_SECRET_KEY='):
                os.environ['DJANGO_SECRET_KEY'] = line.split('=', 1)[1].strip()
                break

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured('Set DJANGO_SECRET_KEY in the environment or in .env.')
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'cursora.apps.CursoraConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'cursora.middleware.ClientIPMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'cursora.context_processors.company_context',
    ]},
}]
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

DATABASES = {'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.environ.get('POSTGRES_DB', 'cursora_db'),
    'USER': os.environ.get('POSTGRES_USER', 'cursora_user'),
    'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
    'HOST': os.environ.get('POSTGRES_HOST', '127.0.0.1'),
    'PORT': os.environ.get('POSTGRES_PORT', '5433'),
}}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ro'
TIME_ZONE = 'Europe/Bucharest'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DATE_FIRMA = {
    'nume': 'Cursora',
    'an_infiintare': '2026',
    'telefon': '0764981698',
    'adresa_sediu': 'București, Lotrioara, nr. 15, sector 3',
    'email_suport': 'office@cursora.ro',
    'numar_angajati': '1',
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
