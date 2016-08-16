from django.views.generic import ListView, DetailView

from .models import My
from {{ project_name }}.views import PublishedViewMixin


class MyListView(ListView, PublishedViewMixin):
    model = My


class MyDetailView(DetailView, PublishedViewMixin):
    model = My
