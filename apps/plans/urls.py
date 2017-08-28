from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add$', views.add),
    url(r'^create$', views.create),
    url(r'^destination/(?P<trip_id>\d+)$', views.trip),
    url(r'^join/(?P<trip_id>\d+)$', views.join)
]
