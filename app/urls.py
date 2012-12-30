# encoding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('app.views',
    url(r'^$', 'index'),
    url(ur'^søk/$', 'search'),
)
