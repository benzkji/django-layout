from django.conf import settings


#CKEDITOR_SETTINGS = {
#    'language': '{{ language }}',
#    'toolbar': 'CMS',
#    'skin': 'moono',
#}

CKEDITOR_SETTINGS = {
    'language': '{{ language }}',
    'toolbar': 'BNZK',
    'toolbar_BNZK': [
        ['Undo', 'Redo'],
        ['cmsplugins', '-', 'ShowBlocks'],
        ['Bold', 'RemoveFormat', ],
        #['Format'],
        ['BulletedList','-','Outdent','Indent'],
        ['Cut','Copy','Paste','PasteText', 'PasteFromWord'],
        [ 'ShowBlocks', 'Source'],
    ],
    'format_tags': 'h2;p',
    'skin': 'moono',
}