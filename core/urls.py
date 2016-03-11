from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = "core"

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url('^demo/', views.demo, name='demo'),
    url('^login/', auth_views.login, name='login', kwargs={'template_name': 'login.html'}),
    url('^logout/', auth_views.logout, name='logout', kwargs={'next_page': '/'}),

    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^search/$', views.search, name='search'),

    url(r'^series/synchronize/$', views.series_synchronize, name='series_synchronize'),
    url(r'^series/(?P<series_id>\d+)/$', views.series, name='series'),
    url(r'^series/(?P<series_id>\d+)/seen/$', views.series_seen, name='series_seen'),
    url(r'^series/(?P<series_id>\d+)/status/$', views.series_status, name='series_status'),
    url(r'^series/(?P<series_id>\d+)/delete/$', views.series_delete, name='series_delete'),
]
