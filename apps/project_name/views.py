from django.http import HttpResponsePermanentRedirect


class LanguageChooserEnhancerMixin(object):
    """
    this calls correct get_absolute_urls in language_chooser tags!
    """
    def get(self, request, **kwargs):
        self.object = self.get_object()
        if hasattr(self.request, 'toolbar'):
            self.request.toolbar.set_object(self.object)
        return super(LanguageChooserEnhancerMixin, self).get(request, **kwargs)



class AutoSlugMixin(object):
    """
    redirect if the slug is no more correct!
    """
    def get(self, request, **kwargs):
        self.object = self.get_object()
        if self.request.path != self.object.get_absolute_url():
            return HttpResponsePermanentRedirect(self.object.get_absolute_url())
        return super(AutoSlugMixin, self).get(request, **kwargs)


class PublishedViewMixin():
    """
    in edit mode, get all, otherwise only published
    """
    def get_queryset(self):
        if self.request.toolbar.edit_mode:
            return self.get_model().objects.all()
        return self.get_model().objects.published()
