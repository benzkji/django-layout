from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
from cms.toolbar.items import Break
from cms.cms_toolbars import PlaceholderToolbar, ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK
from cms.toolbar_base import CMSToolbar


@toolbar_pool.register
class CustomToolbar(CMSToolbar):

    def populate(self):
        admin_menu = self.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER)
        position = admin_menu.find_first(Break, identifier=ADMINISTRATION_BREAK)
        url = reverse('admin:filer_folder_changelist')
        admin_menu.add_sideframe_item(_('Files'), url=url, position=1)

        # blog_menu = self.toolbar.get_or_create_menu("bellevue_blog", "Bellevue Blog",
        #                                                 position=3, )
        # url = reverse('admin:phblog_blogpost_changelist')
        # blog_menu.add_sideframe_item(_('Posts'), url=url)
        # url = reverse('admin:phblog_category_changelist')
        # blog_menu.add_sideframe_item(_('Kategorien'), url=url)
        # url = reverse('admin:phblog_tag_changelist')
        # blog_menu.add_sideframe_item('Tags', url=url)


toolbar_pool.unregister(PlaceholderToolbar)

@toolbar_pool.register
class PlaceholderToolbarNoWizard(PlaceholderToolbar):
    def add_wizard_button(self):
        pass