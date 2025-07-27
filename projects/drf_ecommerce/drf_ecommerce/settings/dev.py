# py
# django
from drf_ecommerce.settings.base import *
# third
from decouple import config
# own

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY_DEV")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG_DEV", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS_DEV", default=['127.0.0.1', 'localhost', 'my_web.com'], cast=lambda v: [host.strip() for host in v.split(',')])

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config("DB_ENGINE_DEV"),
        'NAME': BASE_DIR / config("DB_NAME_DEV"),
    }
}

# config send emails.
EMAIL_BACKEND = config('EMAIL_BACKEND_DEV')
EMAIL_HOST = config('EMAIL_HOST_DEV')
EMAIL_PORT = config('EMAIL_PORT_DEV', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS_DEV', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER_DEV')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD_DEV')