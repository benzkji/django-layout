from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
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

        # misc_menu = self.admin_menu.get_or_create_menu("misc", _("Diverses"),  )

        self.add_crud_menu_item('textblocks', 'textblock', label=_('Texteblöcke'))
        self.add_crud_menu_item('admin', 'logentry', label=_('Admin Log'))
        # self.admin_menu.add_sideframe_item(
        #     _('Projects'),
        #     url=admin_reverse('newsevents_event_changelist')
        # )
        # self.admin_menu.add_sideframe_item(
        #     _('Texte'),
        #     url=admin_reverse('textblocks_textblock_changelist')
        # )

