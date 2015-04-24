from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.DeviceList.as_view(), name='device-list'),
    url(r'^(?P<pk>[0-9]+)/', views.DeviceUpdate.as_view(), name='device-ops'),
]
