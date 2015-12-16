import os
import djcelery
djcelery.setup_loader()

BROKER_HOST = "localhost"
BROKER_BACKEND = "redis"
REDIS_PORT = 6379
REDIS_HOST = "localhost"
BROKER_USER = ""
BROKER_PASSWORD = ""
BROKER_VHOST = "0"
REDIS_DB = 0
REDIS_CONNECT_RETRY = True
CELERY_SEND_EVENTS = True
CELERY_RESULT_BACKEND = 'redis'
CELERY_TASK_RESULT_EXPIRES = 10
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_ALWAYS_EAGER = False
SOCIAL_AUTH_LOGIN_ERROR_URL = '/'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')90zt%&%(8r5_ioesjk6s1%e_h7bzz30crt(80q9^cu%)yv0v='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost"]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'social.apps.django_app.default',
    'Gitpard.apps.repository',
    'Gitpard.apps.analysis',
    'djcelery',
)


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',),
    'PAGE_SIZE': 10,
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.ModelSerializer',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'EXCEPTION_HANDLER': 'Gitpard.apps.repository.utils.custom_exception_handler',
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'Gitpard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_LOGIN_URL = '/auth/login/google-oauth2'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '28157669622-ovlonhqiemin0m19ogd2jf53m1h3mikg'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'x987lgGXn_DcFEpVwtK0N_YL'
SOCIAL_AUTH_URL_NAMESPACE = 'social'

LOGIN_URL = '/auth/login/google-oauth2'
LOGIN_REDIRECT_URL = '/'

WSGI_APPLICATION = 'Gitpard.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
REPO_ROOT = os.path.join(MEDIA_ROOT, 'repositories')
REPORT_ROOT = os.path.join(MEDIA_ROOT, 'reports')
STATIC_ROOT = 'staticfiles'

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    "/home/itis-lab/fight/gitpard/static",
)

if not os.path.exists(REPO_ROOT):
    os.makedirs(REPO_ROOT)
