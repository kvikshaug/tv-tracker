from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

import re

from core import tvdb
from core.models import Show

def index(request):
    series = Show.objects.all().order_by('name')
    active_series = series.filter(local_status='active')
    default_series = series.filter(local_status='default')
    archived_series = series.filter(local_status='archived')
    context = {
        'active_series': active_series,
        'default_series': default_series,
        'archived_series': archived_series,
    }
    return render(request, 'index.html', context)

def show(request, show):
    show = Show.objects.get(id=show)
    context = {'show': show}
    return render(request, 'show.html', context)

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

def add_show(request, id):
    show = tvdb.create_or_update_show(id)
    return redirect('core.views.show', show.id)

def delete_show(request, show):
    show = Show.objects.get(id=show)
    show.delete()
    return redirect('core.views.index')

def last_seen(request):
    show = Show.objects.get(id=request.POST['show'])
    if request.POST['last-seen'] == '' or re.match('^\d+x\d+$', request.POST['last-seen']):
        show.last_seen = request.POST['last-seen']
    show.save()
    return redirect('core.views.show', show.id)

def set_show_status(request, show, status):
    if status not in [s[0] for s in Show.LOCAL_STATUS_CHOICES]:
        raise PermissionDenied

    show = Show.objects.get(id=show)
    show.local_status = status
    show.save()
    return redirect('core.views.index')
