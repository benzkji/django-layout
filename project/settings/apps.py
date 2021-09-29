
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    '{{ project_name }}',

    'axes',
    # 'painless_redirects',
    # 'djangocms_misc',
    'djangocms_misc.basic',
    # 'djangocms_misc.alternate_toolbar',
    'djangocms_misc.admin_style',
    # 'djangocms_misc.global_untranslated_placeholder',
    'formfieldstash',
    'ckeditor_link',
    'ckeditor_link.link_model',
    'mailprotector',
    'textblocks',
    'filer_addons.filer_utils',
    'filer_addons.filer_gui',
    'filer_addons.filer_signals',

    # 'djangocms_baseplugins.baseplugin',
    # 'my_baseplugin',
    # 'djangocms_baseplugins.section',
    # 'djangocms_baseplugins.slider',
    # 'djangocms_baseplugins.gallery',
    #
    # 'djangocms_baseplugins.text',
    # 'djangocms_baseplugins.textimage',
    # 'djangocms_baseplugins.image',
    #
    # 'djangocms_baseplugins.teaser',
    # 'djangocms_baseplugins.iframe',
    # 'djangocms_baseplugins.video',

    'compressor',
    'modeltranslation',
    'ckeditor',

    'filer',
    'easy_thumbnails',

    'cms',
    'menus',
    'classytags',
    'treebeard',
    'sekizai',
    'djangocms_admin_style',

    'django.contrib.admin',
]
