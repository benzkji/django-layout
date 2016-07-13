from split_settings.tools import optional, include

include(
    'base.py',
    'assets.py',
    'hosts.py',
    'apps.py',
    'cms.py',
    'placeholders.py',
    'ckeditor.py',
    '_{{ project_name }}_dev.py',
    optional('local.py'),
    scope=globals()
)
