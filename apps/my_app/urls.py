from django.conf.urls import url

from .views import MyListView, MyDetailView


urlpatterns = [
    url(r'^$', MyListView.as_view(), name='my_list'),
    url(r'^detail/(?P<id>\d+)/(?P<slug>[\w-]+)/$', MyDetailView.as_view(), name='my_detail'),
]
