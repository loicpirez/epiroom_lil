from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^planning$', views.planning),
    #url(r'^getplanning$', views.getplanning),
    url(r'^rooms/(?P<room_id>\d+)$', views.rooms),
    url(r'^users$', views.users),
    url(r'^logs$', views.logs),
    url(r'^cmd$', views.cmd),
]
