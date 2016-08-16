# coding: utf-8
from __future__ import unicode_literals

from cms.menu_bases import CMSAttachMenu,  Menu
from django.conf import settings
from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _

from .models import My


class MyMenu(CMSAttachMenu):
    name = _('My Menu')
    def get_nodes(self, request):
        # better: check if current Site has a BLOG app somewhere...
        nodes = []
        if settings.SITE_ID == 2:
            categories = My.objects.published()
            for cat in categories:
                node = NavigationNode(cat.title, cat.get_absolute_url(), cat.id)
                nodes.append(node)
        return nodes

# menu_pool.register_menu(MyMenu)