from django.conf.urls import path

from .views import MyListView, MyDetailView


urlpatterns = [
    path('', MyListView.as_view(), name='my_list'),
    path('detail/<int:pk>/<slug:slug>/', MyDetailView.as_view(), name='my_detail'),
]
