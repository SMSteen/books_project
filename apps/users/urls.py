from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<id>\d+)$', views.show),
    url(r'^(?P<id>\d+)/edit$', views.edit),
    url(r'^(?P<id>\d+)/update$', views.update),
]