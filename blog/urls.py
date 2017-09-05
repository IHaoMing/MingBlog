#coding:utf-8

from django.conf.urls import url

from . import views
#命名空间
app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^archives/$', views.archives, name='archives'),
    url(r'^about/$', views.about, name='about'),
]
