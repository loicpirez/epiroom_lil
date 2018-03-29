from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^rooms$', views.rooms),
    url(r'^room/(?P<room>[\w -]+)$', views.rooms),
    url(r'^users$', views.users),
    url(r'^user/(?P<user>[\w @.-]+)$', views.users),
    url(r'^bookings$', views.bookings),
    url(r'^booking/(?P<id>[\d]+)$', views.bookings),
    url(r'^dispo$', views.dispo),
    url(r'^dispo/(?P<user>[\w @.-]+)$', views.dispo),
]
