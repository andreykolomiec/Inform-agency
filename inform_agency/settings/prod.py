from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
# ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['PG_DATABASE'],
        'USER': os.environ['PG_USER'],
        'PASSWORD': os.environ['PG_PASSWORD'],
        'HOST': os.environ['PG_HOST'],
        'PORT': int(os.environ['PG_DB_PORT']),
    }
}
