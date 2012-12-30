from django.http import HttpResponse
from django.shortcuts import render

import json

from app import tvdb

def index(request):
    return render(request, 'index.html')


def search(request):
    if request.method == 'GET':
        context = {'series_search_query': request.GET.get('query', '')}
        return render(request, 'search.html', context)
    elif request.method == 'POST':
        result = tvdb.search_series(request.POST['query'])
        return HttpResponse(json.dumps(result))
