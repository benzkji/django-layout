import environ
from split_settings.tools import optional, include


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['localhost', ]),
    DEFAULT_FROM_EMAIL=(str, '{{project_name}}@bnzk.ch'),
    SITE_ID=(int, 1),
)


include(
    'base.py',
    'assets.py',
    'apps.py',
    'cms.py',
    'placeholders.py',
    'plugins.py',
    'ckeditor.py',
    '_{{ project_name }}.py',
    'security.py',
    optional('local.py'),
    scope=globals()
)
