# coding: utf-8
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import PublishedManager


@python_2_unicode_compatible
class My(models.Model):
    title = models.CharField(max_length=255)

    objects = PublishedManager()

    def __str__(self):
        return u'%s' % (self.title, )
