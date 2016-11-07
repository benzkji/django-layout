from django.contrib import admin
from formfieldstash.admin import FormFieldStashMixin
from ckeditor_link.admin import DjangoLinkAdmin

from .models import Link, LINK_FIELDS


NO_TEXT_LINK_FIELDS = list(LINK_FIELDS)
NO_TEXT_LINK_FIELDS.pop(0)


class LinkAdmin(FormFieldStashMixin, DjangoLinkAdmin):
    single_formfield_stash = ('link_type', )
    fieldsets = (
        (None, {'fields': NO_TEXT_LINK_FIELDS}),
    )

    # fix for page widget error! use with cms 3.3.1
    class Media:
        js = ('cms/js/dist/bundle.admin.base.min.js',)

admin.site.register(Link, LinkAdmin)
