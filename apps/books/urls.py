from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^(?P<id>\d+)$', views.show),
    url(r'^(?P<id>\d+)/edit$', views.edit),
    url(r'^(?P<id>\d+)/update$', views.update),
    url(r'^(?P<id>\d+)/delete$', views.destroy),
    url(r'^(?P<id>\d+)/like$', views.like),
    url(r'^(?P<id>\d+)/unlike$', views.unlike),
]