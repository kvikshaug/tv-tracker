# encoding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('core.views',
    url(r'^$', 'index'),
    url(r'^serie/(?P<series>\d+)/$', 'series'),
    url(r'^søk/$', 'search'),
    url(r'^ny/(?P<id>\d+)/$', 'add_series'),
    url(r'^slett/(?P<series>\d+)/$', 'delete_series'),
    url(r'^sist-sett/$', 'last_seen'),
    url(r'^sett-status/(?P<series>\d+)/(?P<status>[a-z]+)/$', 'set_series_status'),
)
