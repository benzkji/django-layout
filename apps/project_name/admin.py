from django.contrib import admin
from django import forms
from django.contrib.admin.models import LogEntry
from formfieldstash.admin import FormFieldStashMixin
from ckeditor_link.admin import DjangoLinkAdmin
from ckeditor_link.link_model.conf import CKEDITOR_LINK_TYPE_CHOICES, CKEDITOR_LINK_STYLE_CHOICES
from django.utils.html import format_html
from django.template.defaultfilters import truncatechars

from .models import Link


MY_CKEDITOR_LINK_TYPE_CHOICES = list(CKEDITOR_LINK_TYPE_CHOICES)
# MY_CKEDITOR_LINK_TYPE_CHOICES.append(
#     ('project', 'Project', )
# )

MY_CKEDITOR_LINK_STYLE_CHOICES = list(CKEDITOR_LINK_STYLE_CHOICES)
# MY_CKEDITOR_LINK_STYLE_CHOICES.append(
#     ('fat_button', 'Fat Button', )
# )

LINK_TYPE_STASH = {
    'cms_page': ['cms_page', 'html_anchor', ],
}


class LinkAdminForm(forms.ModelForm):
    link_type = forms.ChoiceField(
        required=False,
        choices=MY_CKEDITOR_LINK_TYPE_CHOICES,
        widget=forms.Select(
            attrs=get_advanced_stash_attrs('link_type', LINK_TYPE_STASH)
        )
    )
    link_style = forms.ChoiceField(
        required=False,
        choices=CKEDITOR_LINK_STYLE_CHOICES,
    )


@admin.register(Link)
class LinkAdmin(FormFieldStashMixin, DjangoLinkAdmin):
    form = LinkAdminForm

    # OLD TIMES!
    # fix for page widget error! use with cms 3.3.1
    # class Media:
    #     js = ('cms/js/dist/bundle.admin.base.min.js',)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'edited_object', 'action_time', 'user', )
    list_filter =  ('user', 'content_type', )

    def get_title(self, log_entry):
        return truncatechars(str(log_entry), 130)

    def edited_object(self, log_entry):
        obj = log_entry.get_edited_object()
        if obj:
            return format_html('<a href="{}">{}</a>', log_entry.get_admin_url(), truncatechars(str(obj), 70))
        else:
            return '-'

    edited_object.short_description = 'Edited Object'
    edited_object.allow_tags = True
