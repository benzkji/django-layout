# coding: utf-8
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from djangocms_baseplugins.baseplugin.models import AbstractBasePlugin


@python_2_unicode_compatible
class My(AbstractBasePlugin):
    amount = models.CharField(max_length=255)

    def __str__(self):
        text = self.amount
        return self.add_hidden_flag(text)

    # def copy_relations(self, old_instance):
    #     super().copy_relations(old_instance)
    #     # self.images.add(*old_instance.images.all())
    #     for entry in old_instance.teaserimage_set.all():
    #         entry.id = None
    #         entry.save()
    #         self.teaserimage_set.add(entry)
