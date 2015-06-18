
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
        ['cmsplugins', '-', 'ShowBlocks'],
        ['Bold', 'RemoveFormat', ],
        # ['Format'],
        ['BulletedList', 'NumberedList' '-', 'Outdent', 'Indent'],
        ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', ],
        ['ShowBlocks', 'Source'],
    ],
    'format_tags': 'h1;h2;h3;p',
    'skin': 'moono',
}
