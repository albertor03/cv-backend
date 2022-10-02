import os

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

environment = f"backend.routes.{os.getenv('ENV', 'prod')}"
ROOT_URLCONF = environment

DATABASES = {
  'default': {
      'ENGINE': 'djongo',
      'NAME': os.getenv('DB_NAME', ''),
      'CLIENT': {
          'host': f'mongodb+srv://{os.getenv("DB_USER", "")}:{os.getenv("DB_PASS", "")}@{os.getenv("DB_DOMAIN", "")}.mongodb.net/{os.getenv("DB_NAME", "")}?retryWrites=true&w=majority',
          'authMechanism': 'SCRAM-SHA-1'
      }
  },
}

SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(minutes=int(os.getenv('TIMEOUT_TOKEN', 60)))
SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'] = timedelta(minutes=int(os.getenv('TIMEOUT_REFRESH_TOKEN', 10)))

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
