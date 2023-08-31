from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

environment = 'prod'
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
