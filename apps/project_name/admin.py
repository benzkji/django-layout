from django.contrib import admin
from django import forms
from django.contrib.admin.models import LogEntry
from formfieldstash.admin import FormFieldStashMixin
from ckeditor_link.admin import DjangoLinkAdmin
from ckeditor_link.link_model.conf import CKEDITOR_LINK_TYPE_CHOICES, CKEDITOR_LINK_STYLE_CHOICES

from .models import Link


MY_CKEDITOR_LINK_TYPE_CHOICES = list(CKEDITOR_LINK_TYPE_CHOICES)
# MY_CKEDITOR_LINK_TYPE_CHOICES.append(
#     ('project', 'Project', )
# )


class LinkAdminForm(forms.ModelForm):
    link_type = forms.ChoiceField(
        required=False,
        choices=MY_CKEDITOR_LINK_TYPE_CHOICES,
        widget=forms.Select(
            attrs={
                'data-formfield-stash': 'true',
                'data-original-field': 'link_type',
            }
        )
    )
    link_style = forms.ChoiceField(
        required=False,
        choices=CKEDITOR_LINK_STYLE_CHOICES,
    )


@admin.register(Link)
class LinkAdmin(FormFieldStashMixin, DjangoLinkAdmin):
    form = LinkAdminForm
    single_formfield_stash = ('link_type', )

    # fix for page widget error! use with cms 3.3.1
    class Media:
        js = ('cms/js/dist/bundle.admin.base.min.js',)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'edited_object', 'action_time', 'user', )
    list_filter =  ('user', 'content_type', )

    def edited_object(self, log_entry):
        obj = log_entry.get_edited_object()
        if obj:
            return '<a href="{}">{}</a>'.format(log_entry.get_admin_url(), str(obj))
        else:
            return '-'

    edited_object.short_description = 'Edited Object'
    edited_object.allow_tags = True
