# for djangocms-baseplugins, or other plugins, as needed

# if you dont, do migrations on your own! (as with translate!)
DJANGOCMS_BASEPLUGINS_USE_FILER_ADDONS = True


# just in case...
DJANGOCMS_BASEPLUGINS_TRANSLATE = False


IMAGEPLUGIN_DESIGN_FIELDS = ['layout', ]

AUTOCOLUMNSPLUGIN_CHILD_CLASSES = ("TextPlugin", "ImagePlugin", )


# etc
