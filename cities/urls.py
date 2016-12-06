from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^game/$', views.index, name='game'),
  url(r'^login/$', views.login , name='login'),
  url(r'^logout/$', views.logout , name='logout'),
  url(r'^reset/$', views.logout , name='reset'),
]
