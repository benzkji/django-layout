# coding: utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

# from .cms_menus import CategoryMenu


class MyAppHook(CMSApp):
    name = _("My App")
    # menus = [CategoryMenu, ]
    urls = ["my.urls", ]

# apphook_pool.register(MyAppHook)
