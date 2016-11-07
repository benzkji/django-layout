# coding: utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from cms.models.fields import PageField
from django.db import models
from filer.fields.file import FilerFileField


class PublishedBase(models.Model):
    published = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ModifiedBase(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


LINK_TARGET_CHOICES = (
    ('', _("Automatisch")),
    ('_blank', _("Gleiches Fenster")),
    ('_top', _("Neues Fenster")),
    # ('_overlay', _("Overlay")),
)


LINK_TYPE_CHOICES = (
    ('', _("Keiner")),
    ('page', _("Seite")),
    ('file', _("File")),
    ('mailto', _("E-Mail")),
    ('external', _("External URL")),
    ('free', _("Free")),
)


LINK_FIELDS = ('link_text', ('link_type', 'link_target', ), 'page', 'file', 'mailto', 'external', 'free', )


# add target?
class LinkBase(models.Model):
    link_text = models.CharField(verbose_name=_('Link Text'), max_length=255,
                                 blank=True, default='')
    link_type = models.CharField(verbose_name=_('Link'), max_length=20, choices=LINK_TYPE_CHOICES,
                                 blank=True, default='')
    link_target = models.CharField(verbose_name=_('Target'), max_length=20, choices=LINK_TARGET_CHOICES,
                                     blank=True, default='')
    page = PageField(null=True, blank=True)
    file = FilerFileField(null=True, blank=True, related_name='link')
    mailto = models.EmailField(null=True, blank=True)
    external = models.URLField(null=True, blank=True)
    free = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        abstract = True

    def get_link(self):
        if self.link_type:
            for key, display in LINK_TYPE_CHOICES:
                if not key == self.link_type:
                    setattr(self, key, None)
        if self.page:
            if self.page.site.id == settings.SITE_ID:
                return self.page.get_absolute_url()
            else:
                return 'http://' + self.page.site.domain + self.page.get_absolute_url()
        elif self.file:
            return self.file.url
        elif self.external:
            link = self.external
            if not link.startswith('http'):
                link = 'http://%s' % link
            return link
        elif self.mailto:
            return "mailto:%s" % self.mailto

    def get_link_text(self):
        obj = None
        if self.name:
            return self.name
        if self.link_type:
            obj = getattr(self, self.link_type, None)
        elif self.page:
            obj = self.page
        elif self.file:
            obj = self.file
        elif self.external:
            return self.external
        elif self.mailto:
            return self.mailto

        if not object is None:
            return unicode(obj)
        return ''

    def get_link_type(self):
        if self.link_type:
            return self.link_type
        if self.page:
            return "page"
        elif self.file:
            return "file"
        elif self.external:
            return "external"
        elif self.mailto:
            return "mailto"

    def get_link_target(self):
        type = self.get_link_type()
        if type in ['file', 'external']\
                or type == 'page' and not self.page.site.id == settings.SITE_ID:
            return "_blank"
        return ""


class Link(LinkBase):
    class Meta:
        managed = False
