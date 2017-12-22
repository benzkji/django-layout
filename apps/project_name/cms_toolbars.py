# coding: utf-8
from __future__ import unicode_literals

# from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
# from cms.utils.urlutils import admin_reverse
from djangocms_misc.alternate_toolbar.cms_toolbars import AlternateBasicToolbar


toolbar_pool.unregister(AlternateBasicToolbar)


@toolbar_pool.register
class CustomToolbar(AlternateBasicToolbar):

    def add_more_admin_menu_items(self):
        pass
        # self.admin_menu.add_sideframe_item(
        #     _('Projects'),
        #     url=admin_reverse('newsevents_event_changelist')
        # )
