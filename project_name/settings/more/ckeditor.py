
# CKEDITOR_SETTINGS = {
#    'language': '{{ language }}',
#    'toolbar': 'CMS',
#    'skin': 'moono',
# }

CKEDITOR_SETTINGS = {
    'language': '{{ language }}',
    'toolbar': 'BNZK',
    'toolbar_BNZK': [
        ['Undo', 'Redo'],
        ['cmsplugins', ],
        ['Bold', 'RemoveFormat', ],
        # ['Format'],
        ['BulletedList', 'NumberedList' '-', 'Outdent', 'Indent'],
        ['Cut', 'Copy', 'PasteText', ],
        ['cleanup', ],
        ['ShowBlocks', 'Source'],
    ],
    'format_tags': 'h1;h2;h3;p',
    'skin': 'moono',
}
