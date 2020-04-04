import os
from currency_exchange.settings import BASE_DIR

from currency_exchange.settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nq8d7fgytd87fgd8fgydfug0d9fg0dfu9gfdf0du8g!y)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

CELERY_ALWAYS_EAGER = True
CELERY_TASK_ALWAYS_EAGER = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_BACKEND = 'django.core.mail.outbox'
