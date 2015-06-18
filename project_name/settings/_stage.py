from split_settings.tools import include
import os

from base import PROJECT_PATH


include(
    '__init__.py',
    'deploy.py',
    scope=globals()
)

MEDIA_ROOT = os.path.join(PROJECT_PATH, "public", "media")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3'.
        'NAME': "{{project_name}}_stage",  # Or path to db file if sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '{{project_name}}',
        'PASSWORD': 'aaaaaaa',
        'CONN_MAX_AGE': 600,
        # 'STORAGE_ENGINE': "MyISAM",
        # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'HOST': '',
        # Set to empty string for default.
        'PORT': '',
    }
}
