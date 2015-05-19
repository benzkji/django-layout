from base import ugettext


CMS_PLACEHOLDER_CONF = {
    'header_left': {
        'plugins': ['ImagePlugin', ],
        'extra_context': {"size": "600x420"},
        'name': ugettext("Headerbild"),
        # 'language_fallback': True,
    },
    'header_right': {
        'plugins': ['ImagePlugin', ],
        'extra_context': {"size": "240x420"},
        'name': ugettext("Header Rechts"),
        # 'language_fallback': True,
    },
    'left_content': {
        'plugins': ['TeaserPlugin', ],
        'extra_context': {"size": "240x420"},
        'name': ugettext("Inhalt Links"),
        # 'language_fallback': True,
    },
    'header_teaser': {
        'plugins': ['TeaserPlugin', ],
        'extra_context': {"size": "240x420"},
        'name': ugettext("Header Teaser"),
        # 'language_fallback': True,
    },
    'content': {
        "plugins": ['MultiLineTitlePlugin', 'ImageTextPlugin', 'GalleryPlugin', 'TextPlugin',
                    'IframePlugin', 'AccordionPlugin', 'FormPlugin', 'AccordionEntryPlugin',
                    'OfferPlugin', 'RoomOfferPlugin', ],
        'text_only_plugins': ["LinkPlugin", ],
        "extra_context": {"width": 280},
        'name': ugettext("Inhalt"),
        'default_plugins': [
            {
                'plugin_type': 'MultiLineTitlePlugin',
                'values': {
                    'title': 'Der Titel'
                },
            },
            {
                'plugin_type': 'TextPlugin',
                'values': {
                    'body': '<p>Lorem ipsum dolor sit amet...</p>'
                },
            },
            {
                'plugin_type': 'AccordionPlugin',
                'values': {
                },
                'children': [
                    {
                        'plugin_type': 'AccordionEntryPlugin',
                        'values': {
                            'title': 'Accordion Eintrag',
                        },
                        'children': [
                            {
                                'plugin_type': 'TextPlugin',
                                'values': {
                                    'body': '<p>Accordion Text: Lorem ipsum dolor sit amet...</p>'
                                },
                            },
                        ]
                    },
                ]
            },
        ]
    },
}
