from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

import json
import re

from app import tvdb
from app.models import Show, Season, Episode

def index(request):
    context = {'series': Show.objects.all().order_by('name')}
    return render(request, 'index.html', context)

def show(request, show):
    show = Show.objects.get(id=show)
    context = {'show': show}
    return render(request, 'show.html', context)

def search(request):
    q = request.GET.get('query', '')
    series = []
    if len(q) >= 3:
        series = tvdb.search_series(q)
    context = {
        'series_search_query': q,
        'series_search_results': series}
    return render(request, 'search.html', context)

def add_show(request, id):
    show = tvdb.add_show(id)
    return HttpResponseRedirect(reverse('app.views.show', args=[show.id]))

def last_seen(request):
    show = Show.objects.get(id=request.POST['show'])
    if request.POST['last-seen'] == '' or re.match('^\d+x\d+$', request.POST['last-seen']):
        show.last_seen = request.POST['last-seen']
    show.save()
    return HttpResponseRedirect(reverse('app.views.show', args=[show.id]))
