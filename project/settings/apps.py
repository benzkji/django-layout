
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

    'compressor',
    'modeltranslation',

    'filer',
    'easy_thumbnails',

    'cms',
    'menus',
    'classytags',
    'treebeard',
    'sekizai',
    'djangocms_admin_style',

    'djangocms_text_ckeditor',

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',

)
