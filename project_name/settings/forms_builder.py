import os
from base import PROJECT_PATH

FORMS_BUILDER_USE_SITES = False

FORMS_BUILDER_EXTRA_FIELDS = (
    #(199, "django.forms.MultipleChoiceField", "Angebote Spezialfeld"),
    (199, "djangocms_bnzk_offer.fields.OfferMultipleChoiceField", "Angebote Spezialfeld"),
    (299, "djangocms_bnzk_forms_builder.fields.NoField", "Zwischentitel"),
)

#FORMS_BUILDER_EXTRA_WIDGETS = (
#    (199, "djangocms_bnzk_offer.fields.OfferWidget"),
#)