from pathlib import Path
from os import getenv

BASE_DIR = Path(__file__).resolve().parent.parent

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = 'django-insecure-_86yz8)=br_x6$=2eu_@14havrmj@&2wr1sf&rl*g41#dc^ihk'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'user',
    'event',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.user_auth_middleware.UserAuthMiddleware',
    'middleware.api_usage_tracker_middleware.ApiUsageTrackerMiddleware',
]

ROOT_URLCONF = 'muta_event.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'muta_event.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',          
        'USER': 'myuser',       
        'PASSWORD': 'mypassword',
        'HOST': 'db',
        'PORT': '5432',
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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587
EMAIL_HOST_USER = getenv('EMAIL_HOST_USER')  
EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD')  
EMAIL_USE_TLS = True

COOKIE_ENCRYPTION_SECRET =  getenv("COOKIE_ENCRYPTION_SECRET") or 'fallback'
STRIPE_PUBLISHABLE_KEY = getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = getenv("STRIPE_SECRET_KEY")
STRIPE_ENDPOINT_SECRET = getenv("STRIPE_ENDPOINT_SECRET")

SUBSCRIPTION_CONFIG = {
    'FREE':{
        'max_events': 3,
        'max_attendees_per_event': 3
    }
}

FRONTEND_URL = getenv("FRONTEND_URL")