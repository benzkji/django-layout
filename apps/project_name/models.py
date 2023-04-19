from django.db import models
from ckeditor_link.link_model.models import CMSFilerLinkBase


class Link(CMSFilerLinkBase):
    pass


class PublishedBase(models.Model):
    published = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ModifiedBase(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SEOBase(models.Model):
    seo_title = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )
    meta_description = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )

    class Meta:
        abstract = True

    def get_seo_title(self):
        if getattr(self, 'seo_title', None):
            return self.seo_title
        if getattr(self, 'name', None):
            return self.name
        if getattr(self, 'title', None):
            return self.title
        return ''

    def get_seo_description(self):
        if getattr(self, 'meta_description', None):
            return self.meta_description
        if getattr(self, 'description', None):
            return self.description
        return ''
