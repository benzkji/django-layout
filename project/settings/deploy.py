from .apps import INSTALLED_APPS

DEBUG = False
# the following set themselves, normally
# TEMPLATE_DEBUG = False
# THUMBNAIL_DEBUG = False
# COMPRESS_ENABLED = True


def get_git_revision_short_hash():
    import subprocess
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])


if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        release=get_git_revision_short_hash(),
        integrations=[DjangoIntegration()],
    )


# http://www.revsys.com/blog/2015/may/06/django-performance-simple-things/
# TEMPLATE_LOADERS = (
#    ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
# )
