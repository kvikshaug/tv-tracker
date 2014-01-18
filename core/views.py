from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

import re

from core import tvdb
from core.models import Show

def index(request):
    context = {'series': Show.objects.all().order_by('name')}
    return render(request, 'index.html', context)

def show(request, show):
    show = Show.objects.get(id=show)
    context = {'show': show}
    return render(request, 'show.html', context)

def search(request):
    q = request.GET.get('query', '')
    if len(q) < 3:
        raise PermissionDenied

    series = tvdb.search_series(q)
    context = {
        'series_search_query': q,
        'series_search_results': series
    }
    return render(request, 'search.html', context)

def add_show(request, id):
    show = tvdb.add_show(id)
    return redirect('core.views.show', show.id)

def last_seen(request):
    show = Show.objects.get(id=request.POST['show'])
    if request.POST['last-seen'] == '' or re.match('^\d+x\d+$', request.POST['last-seen']):
        show.last_seen = request.POST['last-seen']
    show.save()
    return redirect('core.views.show', show.id)

def sync_series(request):
    for show in Show.objects.all():
        tvdb.add_show(show.tvdbid)
    return redirect('core.views.index')
