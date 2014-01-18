# encoding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('core.views',
    url(r'^$', 'index'),
    url(r'^serie/(?P<show>\d+)/$', 'show'),
    url(r'^søk/$', 'search'),
    url(r'^ny/(?P<id>\d+)/$', 'add_show'),
    url(r'^slett/(?P<show>\d+)/$', 'delete_show'),
    url(r'^sist-sett/$', 'last_seen'),
    url(r'^sett-status/(?P<show>\d+)/(?P<status>[a-z]+)/$', 'set_show_status'),
)
