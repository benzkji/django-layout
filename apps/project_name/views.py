

class PublishedViewMixin():
    def get_queryset(self):
        if self.request.toolbar.edit_mode:
            return self.get_model().objects.all()
        return self.get_model().objects.published()
