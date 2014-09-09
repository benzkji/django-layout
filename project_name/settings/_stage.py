from __init__ import *


MEDIA_ROOT = os.path.join(PROJECT_PATH, "public", "media")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': "{{project_name}}_{{project_name}}_stage",                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '{{project_name}}',
        'PASSWORD': 'aaaaaaa',
        #'STORAGE_ENGINE': "MyISAM",
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}