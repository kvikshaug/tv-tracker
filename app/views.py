from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

import json

from app import tvdb

def index(request):
    return render(request, 'index.html')

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
    tvdb.add_show(id)
    # TODO: Redirect to the *show* page, when that's implemented
    return HttpResponseRedirect(reverse('app.views.index'))
