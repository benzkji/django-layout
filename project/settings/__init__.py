from split_settings.tools import optional, include


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
