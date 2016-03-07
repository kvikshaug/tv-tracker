from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

import re

from core import tvdb
from core.models import Series

def index(request):
    series = Series.objects.prefetch_related(
        'seasons',
        'seasons__episodes',
    ).all()
    active_series = [s for s in series if s.local_status == 'active']
    default_series = [s for s in series if s.local_status == 'default']
    archived_series = [s for s in series if s.local_status == 'archived']
    context = {
        'active_series': active_series,
        'default_series': default_series,
        'archived_series': archived_series,
    }
    return render(request, 'index.html', context)

def increase_seen(request, series):
    series = Series.objects.get(id=series)
    series.increase_seen()
    return redirect('core:index')

def series(request, series):
    series = Series.objects.prefetch_related(
        'seasons',
        'seasons__episodes',
    ).get(id=series)
    context = {'series': series}
    return render(request, 'series.html', context)

def search(request):
    q = request.GET.get('query', '')
    if len(q) < 3:
        raise PermissionDenied

    series = tvdb.search_for_series(q)

    # Sort them - those with air date first, by date, then the rest by name
    series_with_airdate = [s for s in series if s.first_aired is not None]
    series_without_airdate = [s for s in series if s.first_aired is None]
    series_with_airdate_sorted = sorted(series_with_airdate, key=lambda s: s.first_aired, reverse=True)
    series_without_airdate_sorted = sorted(series_without_airdate, key=lambda s: s.name)
    series = series_with_airdate_sorted + series_without_airdate_sorted

    context = {
        'series_search_query': q,
        'series_search_results': series
    }
    return render(request, 'search.html', context)

def add_series(request, id):
    series = tvdb.create_or_update_series(id)
    return redirect('core:series', series.id)

def delete_series(request, series):
    series = Series.objects.get(id=series)
    series.delete()
    return redirect('core:index')

def last_seen(request):
    series = Series.objects.get(id=request.POST['series'])
    if request.POST['last-seen'] == '' or re.match('^\d+x\d+$', request.POST['last-seen']):
        series.last_seen = request.POST['last-seen']
    series.save()
    return redirect('core:series', series.id)

def set_series_status(request, series, status):
    if status not in [s[0] for s in Series.LOCAL_STATUS_CHOICES]:
        raise PermissionDenied

    series = Series.objects.get(id=series)
    series.local_status = status
    series.save()
    return redirect('core:index')
