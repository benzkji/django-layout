import os
from base import PROJECT_PATH

DEBUG = True
THUMBNAIL_DEBUG = True
FOLDERLESS_DEBUG = True

# set this to True to test live behaviour
COMPRESS_ENABLED = False
# more live behavious, if you pleas..
# from deploy import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3'.
        'NAME': os.path.join(PROJECT_PATH, "dev_database.db"),  # Or path to db file if sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'HOST': '',
        # Set to empty string for default.
        'PORT': '',
    }
}
