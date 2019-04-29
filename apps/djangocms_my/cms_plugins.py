# coding: utf-8
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from djangocms_baseplugins.baseplugin.cms_plugins import BasePluginMixin
from djangocms_baseplugins.baseplugin.utils import build_baseplugin_fieldset
from djangocms_baseplugins.baseplugin import defaults

from .models import My


@plugin_pool.register_plugin
class MyPlugin(BasePluginMixin, CMSPluginBase):
    model = My
    name = _(u'My')
    render_template = "djangocms_baseplugins/my.html"
    fieldsets = build_baseplugin_fieldset(**{
        'design': ['background', ],  # create a form if you want dropdowns!
        'content': ['amount', ],
        'advanced': defaults.BASEPLUGIN_ADVANCED_FIELDS,
    })
