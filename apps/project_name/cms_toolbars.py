# coding: utf-8
from __future__ import unicode_literals

# from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
# from cms.utils.urlutils import admin_reverse
from djangocms_misc.alternate_toolbar.cms_toolbars import AlternateBasicToolbar


toolbar_pool.unregister(AlternateBasicToolbar)


@toolbar_pool.register
class CustomToolbar(AlternateBasicToolbar):

    def add_crud_menu_item(self, app, model, menu=None, label=None, view='changelist'):
        if not menu:
            menu = self.admin_menu
        if not label:
            label = model
        if self.request.user.has_perm('{}.view_{}'.format(app, model)):
            menu.add_sideframe_item(
                label,
                url=reverse('admin:{}_{}_{}'.format(app, model, view)),
            )

    def add_more_admin_menu_items(self):

        self.add_crud_menu_item('admin', 'log', label='Admin Log')

        # self.admin_menu.add_sideframe_item(
        #     _('Projects'),
        #     url=admin_reverse('newsevents_event_changelist')
        # )
        # self.admin_menu.add_sideframe_item(
        #     _('Texte'),
        #     url=admin_reverse('textblocks_textblock_changelist')
        # )

