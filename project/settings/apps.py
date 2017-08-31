
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    '{{ project_name }}',
    # 'djangocms_pluginbase.section',
    # 'djangocms_pluginbase.slider',
    # 'djangocms_pluginbase.gallery',
    #
    # 'djangocms_pluginbase.text',
    # 'djangocms_pluginbase.textimage',
    # 'djangocms_pluginbase.image',
    #
    # 'djangocms_pluginbase.teaser',
    # 'djangocms_pluginbase.iframe',
    # 'djangocms_pluginbase.video',

    'compressor',
    'modeltranslation',
    'formfieldstash',
    'ckeditor',

    'filer',
    'easy_thumbnails',

    'cms',
    'menus',
    'classytags',
    'treebeard',
    'sekizai',
    'djangocms_admin_style',


    # Uncomment the next line to enable the admin:
    'django.contrib.admin',

)
