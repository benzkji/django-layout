from split_settings.tools import include


include(
    '__init__.py',
    'deploy.py',
    scope=globals()
)

ENV = 'stage'

ALLOWED_HOSTS = (
    '.stage.bnzk.ch',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3'.
        'NAME': "{{project_name}}_stage",  # Or path to db file if sqlite3.
        # mysl only
        # 'USER': '{{project_name}}',
        # 'PASSWORD': 'aaaaaaa',
        # 'CONN_MAX_AGE': 0,  # set 0 if using gevent and no connection pooling!
        # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        # 'HOST': '',
        # Set to empty string for default.
        # 'PORT': '',
    }
}
