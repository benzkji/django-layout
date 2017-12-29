# coding: utf-8
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from cms.models.pluginmodel import CMSPlugin


@python_2_unicode_compatible
class My(CMSPlugin):
    amount = models.CharField(max_length=255)

    def __str__(self):
        return u'%s Columns' % (self.amount, )
