# coding: utf-8
from __future__ import unicode_literals

from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils.text import slugify

from {{ project_name }}.managers import PublishedManager


@python_2_unicode_compatible
class My(models.Model):
    title = models.CharField(max_length=255)

    objects = PublishedManager()

    class Meta:
        ordering = ('-date', )

    def get_slug(self):
        return slugify(self.title)

    def get_absolute_url(self):
        return reverse('my_detail', args=(self.id, self.get_slug()))

    def __str__(self):
        return u'%s' % (self.title, )
