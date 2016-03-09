import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'
ALLOWED_HOSTS = ['tv.kvikshaug.no']
SECRET_KEY = os.environ['SECRET_KEY']

TIME_ZONE = 'Europe/Oslo'
LANGUAGE_CODE = 'en-us' # See http://www.i18nguy.com/unicode/language-identifiers.html
USE_I18N = True
USE_L10N = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'build')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

RAVEN_CONFIG = {
    'dsn': os.environ['RAVEN_DSN'],
}

TVDB_API_KEY = os.environ['TVDB_API_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'tv',
        'USER': 'postgres',
        'HOST': 'postgis',
        'PORT': 5432,
    },
}

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',

            'project.context_processors.last_update',
        ],
    },
}]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'raven.contrib.django',

    'core',
    'thetvdb',
]

# Logging strategy:
# - All events are verbosely stored in a local file (note that this logfile is currently not persistent)
# - INFO events are also sent to papertrail
# - Events logged by the local project are additionally explicitly sent to Sentry
# - Uncaught exceptions are implicitly sent to Sentry by Raven (no logging configuration is needed for that)
LOGGING = {
    'version': 1,
    # Never disable existing loggers, that will silence logs you want
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
        'verbose': {
            'format': '%(levelname)s (%(name)s) %(asctime)s\n%(pathname)s:%(lineno)d in %(funcName)s\n%(message)s\n'
        },
    },

    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
            'formatter': 'verbose',
        },
        'papertrail': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'simple',
            'address': ('logs2.papertrailapp.com', 58442),
        },
        'sentry': {
            'level': 'DEBUG',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
    },
    'loggers': {
        # Only our own events include the sentry handler
        'tv': {
            'level': 'DEBUG',
            'handlers': ['file', 'papertrail', 'sentry'],
            'propagate': False,
        },

        # Djangos DB backend outputs all SQL-statements to DEBUG; limit to INFO
        'django.db.backends': {
            'level': 'INFO',
            'handlers': ['file', 'papertrail'],
            'propagate': False,
        },

        # Ignore the very verbose template DEBUG statements which include failed context lookups
        'django.template': {
            'level': 'INFO',
            'handlers': ['file', 'papertrail'],
            'propagate': False,
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['file', 'papertrail'],
    }
}
