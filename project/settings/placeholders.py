from .base import ugettext


CMS_PLACEHOLDER_CONF = {
    'home_content': {
        'plugins': [
            'HomeImageTeaserPlugin',
            'MultiColumnTeaserPlugin',
            'ColumnTeaserPlugin',
            'MultiColumnImageTeaserPlugin',
            'ColumnImageTeaserPlugin',
        ],
        'extra_context': {"size": "600x420"},
        'name': ugettext("Home Inhalt"),
        'language_fallback': False,
    },
    'header_image': {
        'plugins': [
            'ImagePlugin',
        ],
        # 'extra_context': {"size": "600x420"},
        'name': ugettext("Headerbild"),
        'language_fallback': True,
    },
    'content': {
        'plugins': [
            'ImagePlugin',
            'TextImagePlugin',
            'TextPlugin',
        ],
        # 'extra_context': {"size": "600x420"},
        # default_plugins: []
        'name': ugettext("Inhalt"),
        'language_fallback': False,
    },
}
