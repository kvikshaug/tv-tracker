# encoding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('core.views',
    url(r'^$', 'index'),
    url(r'^serie/(?P<show>\d+)/$', 'show'),
    url(r'^søk/$', 'search'),
    url(r'^ny/(?P<id>\d+)/$', 'add_show'),
    url(r'^sist-sett/$', 'last_seen'),
    url(r'^synkroniser/$', 'sync_series'),
)
