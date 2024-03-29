import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "test-dev")

DEBUG = bool(int(os.environ.get("DEBUG", default=1)))

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ['https://*.domivka.org.ua', 'https://*.127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'public',
    'user',
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'public.middleware.SEOMiddleware'
]

ROOT_URLCONF = 'real_estate_server.urls'

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

WSGI_APPLICATION = 'real_estate_server.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "127.0.0.1"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

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

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'uk'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

EMAIL_CONFIRM = True
SERVER_EMAIL = 'domivka@domivka.org.ua'
DEFAULT_FROM_EMAIL = 'domivka@domivka.org.ua'
# if DEBUG:
#     EMAIL_USE_TLS = True
#     EMAIL_HOST = 'smtp.gmail.com'
#     EMAIL_HOST_USER = 'evgeniy.python.developer@gmail.com'
#     EMAIL_HOST_PASSWORD = 'iemmevdatpsepdxr'
#     EMAIL_PORT = 587
# else:
#     EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#     EMAIL_USE_SSL = True
#     EMAIL_HOST = 'smtp.hostinger.com'
#     EMAIL_HOST_USER = 'domivka@domivka.org.ua'
#     EMAIL_HOST_PASSWORD = 'FfnNm]NUfd_42.^a'
#     EMAIL_PORT = 465

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_HOST_USER = 'domivka@domivka.org.ua'
EMAIL_HOST_PASSWORD = 'FfnNm]NUfd_42.^a'
EMAIL_PORT = 465

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
