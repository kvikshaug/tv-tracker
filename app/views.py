from django.http import HttpResponse
from django.shortcuts import render

import json

def index(request):
    return render(request, 'index.html')


def search(request):
    return HttpResponse(json.dumps(['foo', 'bar']))
