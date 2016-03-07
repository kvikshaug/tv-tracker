from django.conf.urls import include, url

from . import views

app_name="core"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^se-episode/(?P<series>\d+)/$', views.increase_seen, name='increase_seen'),
    url(r'^serie/(?P<series>\d+)/$', views.series, name='series'),
    url(r'^søk/$', views.search, name='search'),
    url(r'^ny/(?P<id>\d+)/$', views.add_series, name='add_series'),
    url(r'^slett/(?P<series>\d+)/$', views.delete_series, name='delete_series'),
    url(r'^sist-sett/$', views.last_seen, name='last_seen'),
    url(r'^sett-status/(?P<series>\d+)/(?P<status>[a-z]+)/$', views.set_series_status, name='set_series_status'),
]
