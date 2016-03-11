from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

import re

from core.models import Series
from thetvdb import tvdb

def dashboard(request):
    series = Series.objects.prefetch_related('episodes').all()
    active_series = [s for s in series if s.local_status == 'active']
    default_series = [s for s in series if s.local_status == 'default']
    archived_series = [s for s in series if s.local_status == 'archived']
    context = {
        'active_series': active_series,
        'default_series': default_series,
        'archived_series': archived_series,
    }
    return render(request, 'home/dashboard.html', context)

def search(request):
    query = request.GET.get('query', '').strip()
    if len(query) < 3:
        series = []
    else:
        series = tvdb.search_for_series(query)

        # Sort them - those with air date first, by date, then the rest by name
        series_with_airdate = [s for s in series if s.first_aired is not None]
        series_without_airdate = [s for s in series if s.first_aired is None]
        series_with_airdate_sorted = sorted(series_with_airdate, key=lambda s: s.first_aired, reverse=True)
        series_without_airdate_sorted = sorted(series_without_airdate, key=lambda s: s.name)
        series = series_with_airdate_sorted + series_without_airdate_sorted

    context = {
        'series_search_query': query,
        'series_search_results': series
    }
    return render(request, 'home/search.html', context)

def series_synchronize(request):
    series = tvdb.create_or_update_series(int(request.GET['tvdbid']))
    return redirect('core:series', series.id)

def series(request, series_id):
    series = Series.objects.prefetch_related('episodes').get(id=series_id)
    context = {'series': series}
    return render(request, 'home/series.html', context)

def series_seen(request, series_id):
    series = Series.objects.get(id=series_id)

    if 'increment' in request.GET:
        series.move_seen('next')
        return redirect('core:dashboard')
    elif 'decrement' in request.GET:
        series.move_seen('previous')
        return redirect('core:dashboard')
    elif 'last-seen' in request.POST:
        if request.POST['last-seen'] == '' or re.match('^\d+x\d+$', request.POST['last-seen']):
            series.last_seen = request.POST['last-seen']
        series.save()
        return redirect('core:series', series.id)
    else:
        return redirect('core:dashboard')

def series_status(request, series_id):
    status = request.GET.get('status', '')
    if status not in [s[0] for s in Series.LOCAL_STATUS_CHOICES]:
        raise PermissionDenied

    series = Series.objects.get(id=series_id)
    series.local_status = status
    series.save()
    return redirect('core:dashboard')

def series_delete(request, series_id):
    series = Series.objects.get(id=series_id)
    series.delete()
    return redirect('core:dashboard')
