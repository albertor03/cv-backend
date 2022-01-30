from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

environment = f"backend.routes.{os.environ['ENV']}"
ROOT_URLCONF = environment

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = f"{BASE_DIR.parent}/media/"
MEDIA_ROOT = BASE_DIR.parent / 'media/'

DATABASES = {
  'default': {
      'ENGINE': 'djongo',
      'NAME': os.environ["DB_NAME"],
      'CLIENT': {
          'host': f'mongodb+srv://{os.environ["DB_USER"]}:{os.environ["DB_PASS"]}@{os.environ["DB_DOMAIN"]}.mongodb.net/{os.environ["DB_NAME"]}?retryWrites=true&w=majority',
          'authMechanism': 'SCRAM-SHA-1'
      }
  },
}

SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(minutes=int(os.environ['TIMEOUT_TOKEN']))
SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'] = timedelta(minutes=int(os.environ['TIMEOUT_REFRESH_TOKEN']))
