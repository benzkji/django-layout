from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<slug>[a-z0-9]+)/$', WhatEver.as_view(), name='whatever'),
]
