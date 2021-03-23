from django.urls import reverse_lazy


TEXTBLOCKS_CKEDITORJS_URL = '/static/ckeditor/ckeditor/ckeditor.js'

CKEDITOR_LINK_MODEL = '{{ project_name }}.models.Link'
CKEDITOR_LINK_IFRAME_URL = reverse_lazy('admin:{{ project_name }}_link_add')
CKEDITOR_LINK_VERIFY_URL = reverse_lazy('admin:{{ project_name }}_link_verify')


CKEDITOR_CONFIGS = {
    'default': {
        'djangolinkIframeURL': CKEDITOR_LINK_IFRAME_URL,
        'djangolinkVerifyURL': CKEDITOR_LINK_VERIFY_URL,
        'djangolinkFallbackField': 'free',
        'disallowedContent': 'a[style]; pre[style]; h1[style]; h2[style]; h3[style]; p[style]; ul[style]; ol[style]; li[style]',
        'extraPlugins': ','.join(
            [
                # your extra plugins here
                'djangolink',
            ]),
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Maximize'],
            ['Format'],
            ['Bold', ],
            ['BulletedList', ],
            ['DjangoLink', 'Unlink'],
            ['Cut', 'Copy', 'PasteText', ],
            ['cleanup', ],
            ['ShowBlocks', 'Source'],
        ],
        'format_tags': 'h2;p',
        'width': '730',
    }
}
