# Boilerplate imports of preceding prod settings
from project.settings_prod import *

DEBUG = True
ALLOWED_HOSTS = ['*']
RAVEN_CONFIG['dsn'] = None

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    'DISABLE_PANELS': [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
}

INSTALLED_APPS = [
    'werkzeug_debugger_runserver',
    'debug_toolbar',
] + INSTALLED_APPS

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
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        # Djangos DB backend outputs all SQL-statements to DEBUG; limit to INFO
        'django.db.backends': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },

        # Ignore the very verbose template DEBUG statements which include failed context lookups
        'django.template': {
            'level': 'INFO',
            'handles': ['file'],
            'propagate': False,
        },
    },
    # Default behavior: log everything to console, but nowhere else
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
}
