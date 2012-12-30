# encoding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('app.views',
    url(r'^$', 'index'),
    url(ur'^serie/(?P<show>\d+)/$', 'show'),
    url(ur'^søk/$', 'search'),
    url(ur'^ny/(?P<id>\d+)/$', 'add_show'),
)
