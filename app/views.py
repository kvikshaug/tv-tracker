from django.http import HttpResponse
from django.shortcuts import render

import json

from app import tvdb

def index(request):
    return render(request, 'index.html')

def search(request):
    if request.method == 'GET':
        q = request.GET.get('query', '')
        if len(q) >= 3:
            results = tvdb.search_series(q)
        context = {'series_search_query': q}
        return render(request, 'search.html', context)
    elif request.method == 'POST':
        # TBD
        pass
