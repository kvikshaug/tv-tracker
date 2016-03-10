from django.conf.urls import url

from . import views

app_name = "core"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),

    url(r'^series/synchronize/$', views.series_synchronize, name='series_synchronize'),
    url(r'^series/(?P<series_id>\d+)/$', views.series, name='series'),
    url(r'^series/(?P<series_id>\d+)/seen/increase/$', views.series_seen_increase, name='series_seen_increase'),
    url(r'^series/(?P<series_id>\d+)/seen/set/$', views.series_seen_set, name='series_seen_set'),
    url(r'^series/(?P<series_id>\d+)/status/$', views.series_status, name='series_status'),
    url(r'^series/(?P<series_id>\d+)/delete/$', views.series_delete, name='series_delete'),
]
