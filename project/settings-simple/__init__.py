from split_settings.tools import optional, include

include(
    "base.py",
    "assets.py",
    "hosts.py",
    "apps.py",
    "_{{ project_name }}_dev.py",
    optional("local.py"),
    scope=globals(),
)
