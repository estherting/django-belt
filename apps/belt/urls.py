from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main$', views.main),
    url(r'^register/process$', views.register),
    url(r'^signin/process$', views.signin),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.addTravel),
    url(r'^travels/add/process$', views.addTravel_process),
    url(r'^travels/destination/(?P<id>\d+)$', views.destination),
    url(r'^travels/join/(?P<id>\d+)$', views.join),
    url(r'^travels/delete/(?P<id>\d+)$', views.delete),
    url(r'^logout$', views.logout),
]
