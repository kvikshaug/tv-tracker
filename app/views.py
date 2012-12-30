from django.http import HttpResponse
from django.shortcuts import render

import json

from app import tvdb

def index(request):
    return render(request, 'index.html')


def search(request):
    result = tvdb.search_series(request.POST['query'])
    return HttpResponse(json.dumps(result))
