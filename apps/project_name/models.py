# coding: utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from cms.models.fields import PageField
from django.db import models
from django.conf import settings
from filer.fields.file import FilerFileField
from ckeditor_link.link_model.models import CMSFilerLinkBase


class PublishedBase(models.Model):
    published = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ModifiedBase(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Link(CMSFilerLinkBase):
    pass
