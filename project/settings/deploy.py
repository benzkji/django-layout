# common for all deployment settings
# from base import TEMPLATE_LOADERS

DEBUG = False
# the following set themselves, normally
# TEMPLATE_DEBUG = False
# THUMBNAIL_DEBUG = False
# COMPRESS_ENABLED = True

# the raven for the sentry.io
INSTALLED_APPS.insert(0, 'raven.contrib.django.raven_compat')

# http://www.revsys.com/blog/2015/may/06/django-performance-simple-things/
# TEMPLATE_LOADERS = (
#    ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
# )

