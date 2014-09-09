
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    'parkhotel',

    # first, as we need to re-register the admin
    'forms_builder.forms',
    'adminsortable',
    'robots',

    'djangocms_bnzk_title',
    'djangocms_bnzk_image',
    'djangocms_bnzk_imagetext',
    'djangocms_bnzk_file',
    'djangocms_bnzk_accordion',
    'djangocms_bnzk_iframe',
    'djangocms_bnzk_teaser',
    'djangocms_bnzk_gallery',
    'djangocms_bnzk_offer',
    'djangocms_bnzk_room',
    'djangocms_bnzk_forms_builder',

    'djangocms_text_ckeditor',
    'djangocms_link',
    #'djangocms_accordion',

    'south',
    'cms',
    'menus',
    'classytags',
    'mptt',
    'sekizai',
    'djangocms_admin_style',
    'compressor',
    'modeltranslation',

    'painless_redirects',
    'folderless',
    'folderless.test_app',
    'easy_thumbnails',
    'easy_thumbnails.optimize',

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',

)