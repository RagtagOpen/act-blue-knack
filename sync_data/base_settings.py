import os

import raven

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    ''
)

ALLOWED_HOSTS = ['arcane-ridge-14075.herokuapp.com', '127.0.0.1', 'localhost']

DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'raven.contrib.django.raven_compat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sync_data.urls'

WSGI_APPLICATION = 'sync_data.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# ActBlue credentials. DO NOT DEPLOY THIS WITHOUT SETTING ENV VARS
ACTBLUE_USERNAME = os.environ.get('DJANGO_ACTBLUE_USERNAME', 'testuser')
ACTBLUE_PASSWORD = os.environ.get('DJANGO_ACTBLUE_PASSWORD', 'testpassword')

if os.environ.get('SENTRY_DSN'):
    RAVEN_CONFIG = {
        'dsn': os.environ.get('SENTRY_DSN'),
    }
    if os.environ.get('SENTRY_ENVIRONMENT'):
        RAVEN_CONFIG['environment'] = 'SENTRY_ENVIRONMENT'

    if os.environ.get('HEROKU_SLUG_COMMIT'):
        RAVEN_CONFIG['release'] = os.environ.get('HEROKU_SLUG_COMMIT')
    else:
        try:
            RAVEN_CONFIG['release'] = raven.fetch_git_sha(
                os.path.abspath(os.pardir)
            )
        except raven.exceptions.InvalidGitRepository:
            pass  # couldn't find the git repo
