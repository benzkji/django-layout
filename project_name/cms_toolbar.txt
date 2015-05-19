from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
from cms.toolbar.items import Break
from cms.cms_toolbar import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK
from cms.toolbar_base import CMSToolbar


"""
example custom toolbar
@toolbar_pool.register
class CustomToolbar(CMSToolbar):

    def populate(self):
        admin_menu = self.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER)
        position = admin_menu.find_first(Break, identifier=ADMINISTRATION_BREAK)

        #url = reverse('admin:folderless_file_changelist')
        #admin_menu.add_sideframe_item(_('Files'), url=url, position=1)

        #url = reverse('admin:forms_form_changelist')
        #admin_menu.add_sideframe_item(_('Forms'), url=url, position=2)

        #menu = admin_menu.get_or_create_menu('poll-menu', _('Polls'), )
        #url = reverse('admin:polls_poll_changelist')
        #menu.add_sideframe_item(_('Poll overview'), url=url)
        #admin_menu.add_break('poll-break', position=menu)

"""
