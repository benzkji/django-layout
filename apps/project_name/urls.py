from django.conf.urls.static import static
from django.conf.urls import patterns, include
from django.conf import settings

from django.contrib import admin


# maybe use i18npatterns?!
urlpatterns = [
    '',  # dont remove it, it's the prefix!
    # (r'', include('{{ project_name }}.apps.')),
    url(r'^(?P<slug>[a-z0-9]+)/$', WhatEver.as_view(), name='whatever'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
