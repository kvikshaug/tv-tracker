from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
import re

from core.models import Watching, Series
from thetvdb import tvdb
from thetvdb.exceptions import TVDBIDDoesNotExist

def index(request):
    if request.user.is_authenticated():
        return redirect('core:dashboard')

    return render(request, 'index.html')

def demo(request):
    DEMO_USERNAME = 'demouser'
    DEMO_PASSWORD = ''
    demo_user, created = User.objects.get_or_create(username=DEMO_USERNAME, defaults={
        'first_name': '',
        'last_name': '',
        'email': '',
    })
    demo_user.set_password(DEMO_PASSWORD)
    demo_user.save()

    auth_user = authenticate(username=DEMO_USERNAME, password=DEMO_PASSWORD)
    login(request, auth_user)
    return redirect('core:dashboard')

@login_required
def dashboard(request):
    watches = request.user.watches.select_related('series').prefetch_related('series__episodes').all()
    active_series = [s for s in watches if s.status == 'active']
    default_series = [s for s in watches if s.status == 'default']
    archived_series = [s for s in watches if s.status == 'archived']
    context = {
        'active_series': active_series,
        'default_series': default_series,
        'archived_series': archived_series,
    }
    return render(request, 'home/dashboard.html', context)

@login_required
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

@login_required
def watching_start(request):
    try:
        tvdbid = int(request.GET['tvdbid'])
        series = Series.create_or_sync(tvdbid)
        watching, created = Watching.objects.get_or_create(user=request.user, series=series)
        return redirect('core:watching', watching.id)
    except TVDBIDDoesNotExist:
        messages.info(request, 'tvdbid_invalid')
        return redirect('core:dashboard')

@login_required
def watching(request, watching_id):
    watching = Watching.objects.select_related(
        'series',
    ).prefetch_related(
        'series__episodes',
    ).get(id=watching_id)
    context = {'watching': watching}
    return render(request, 'home/series.html', context)

@login_required
def watching_seen(request, watching_id):
    watching = Watching.objects.get(id=watching_id)

    if 'increment' in request.GET:
        watching.move_seen('next')
        return redirect('core:dashboard')
    elif 'decrement' in request.GET:
        watching.move_seen('previous')
        return redirect('core:dashboard')
    elif 'last-seen' in request.POST:
        if request.POST['last-seen'] == '' or re.match('^\d+x\d+$', request.POST['last-seen']):
            watching.last_seen = request.POST['last-seen']
        watching.save()
        return redirect('core:watching', watching.id)
    else:
        return redirect('core:dashboard')

@login_required
def watching_status(request, watching_id):
    status = request.GET.get('status', '')
    if status not in [s[0] for s in Watching.STATUS_CHOICES]:
        raise PermissionDenied

    watching = Watching.objects.get(id=watching_id)
    watching.status = status
    watching.save()
    return redirect('core:dashboard')

@login_required
def watching_stop(request, watching_id):
    Watching.objects.get(id=watching_id).delete()
    return redirect('core:dashboard')
