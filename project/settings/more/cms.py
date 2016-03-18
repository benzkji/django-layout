from base import ugettext


CMS_TEMPLATES = (
    ('{{project_name}}/standard.html', ugettext('Standard')),
    ('{{project_name}}/home.html', ugettext('Homepage')),
)

CMS_CACHE_DURATIONS = {
    'content': 180,
    'menus': 180,
    'permissions': 180,
}

# CMS_CACHE_PREFIX = "cms-" default

CMS_PAGE_CACHE = True
CMS_PLACEHOLDER_CACHE = True
CMS_PLUGIN_CACHE = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'de'
LANGUAGES = (
    ('de', ugettext(u"Deutsch")),
    ('en', ugettext(u"English")),
    ('fr', ugettext(u"Francais")),
)

CMS_LANGUAGES = {
    1: [
        {
            'code': 'de',
            'name': ugettext('Deutsch'),
            'fallbacks': ['en', 'fr'],
            'public': True,
        },
        {
            'code': 'en',
            'name': ugettext('English'),
            'fallbacks': ['fr', 'de'],
            'public': True,
        },
        {
            'code': 'fr',
            'name': ugettext('French'),
            'fallbacks': ['en', 'de'],
            'public': True,
        },
    ],
}

# CMS_PLUGIN_PROCESSORS = (
#    '{{project_name}}.plugin_processors.default_div',
# )
