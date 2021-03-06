# coding: utf-8

import os
import sys

# just in case - know the defaults ;-)
# import django.conf.global_settings as DEFAULT_SETTINGS

PROJECT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            '../../')
sys.path.append(os.path.join(PROJECT_PATH, 'apps/'))

# the fake
ugettext = lambda s: s  # noqa

ADMINS = [
    # no more! raven FTW. ('BNZK', 'support@bnzk.ch'),
]
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL = '{{project_name}}@bnzk.ch'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# opposite of DEBUG!
# HTML_MINIFY = True
# add p when needed
# EXCLUDE_TAGS_FROM_MINIFYING = ['custom', 'pre', 'textarea', 'p', 'script', 'style', ]
KEEP_COMMENTS_ON_MINIFYING = True

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

TEXTBLOCKS_SHOWKEY = True

# enable when behind nginx proxy
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

# SENTRY_DSN = 'https://xxxxxx@sentry.io/1416363'
SENTRY_DSN = False

def get_git_describe():
    import subprocess
    return subprocess.check_output(['git', 'describe', '--tags']).strip()

VERSION = get_git_describe()

INTERNAL_IPS = (
    '127.0.0.1',
    '0.0.0.0',
)

MIGRATION_MODULES = {
    'textblocks': 'apps.{{ project_name }}.migrations_textblocks',
    # 'image': 'apps.{{ project_name }}.migrations_plugins.image',
}

ROOT_URLCONF = 'project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = '{{project_name}}.wsgi.application'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
# only use when having redis or file cache backend!
# SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Zurich'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = '{{ secret_key }}'

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.middleware.locale.LocaleMiddleware',
    # what is this in django 1.8? 'django.middleware.doc.XViewMiddleware',

    # django cms specific
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',

    # 'painless_redirects.middleware.ManualRedirectMiddleware',
    # 'painless_redirects.middleware.ForceSiteDomainRedirectMiddleware',

    'axes.middleware.AxesMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',
                'djangocms_misc.basic.context_processors.get_env',
                '{{ project_name }}.context_processors.general_contextor',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                # 'django.template.loaders.eggs.Loader',
            ]
        },
    },
]


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
"""
