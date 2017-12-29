# coding: utf-8
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import My


class MyPlugin(CMSPluginBase):
    model = My
    name = _(u'My')
    render_template = "djangocms_my/my.html"
    text_enabled = False

    def render(self, context, instance, placeholder):
        context['plugin'] = self
        context['instance'] = instance
        context['placeholder'] = placeholder
        return context


plugin_pool.register_plugin(MyPlugin)
