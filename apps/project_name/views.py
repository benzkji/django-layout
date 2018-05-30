from django.http import HttpResponsePermanentRedirect


class AutoSlugMixin(object):

    def get(self, request, **kwargs):
        self.object = self.get_object()
        if self.request.path != self.object.get_absolute_url():
            return HttpResponsePermanentRedirect(self.object.get_absolute_url())
        return super(AutoSlugMixin, self).get(request, **kwargs)


class PublishedViewMixin():
    def get_queryset(self):
        if self.request.toolbar.edit_mode:
            return self.get_model().objects.all()
        return self.get_model().objects.published()
