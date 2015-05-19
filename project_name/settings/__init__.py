from split_settings.tools import optional, include

include(
    'base.py',
    'assets.py',
    'hosts.py',
    'cms.py',
    'apps.py',
    '_dev.py',
    optional('local.py'),
    scope=globals()
)
