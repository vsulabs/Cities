from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^start/$', views.index, name='index'),
  url(r'^game/$', views.game, name='game'),
  url(r'^login/$', views.login, name='login'),
  url(r'^logout/$', views.logout, name='logout'),
  url(r'^reset/$', views.reset, name='reset'),
]
