from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from . import demo
from .forms import CaptchaForm
from .models import Watching, Series
from thetvdb import tvdb
from thetvdb.exceptions import TVDBIDDoesNotExist

def intro(request):
    if request.user.is_authenticated():
        return redirect('core:dashboard')

    if request.method == 'GET':
        return render(request, 'intro.html')
    elif request.method == 'POST':
        # This is the custom login view which also accepts the case of an empty password
        user = authenticate(
            username=request.POST.get('username', '').strip(),
            password=request.POST.get('password', '').strip(),
        )
        if user is None:
            messages.info(request, 'invalid_authentication')
            return redirect('core:intro')
        else:
            login(request, user)
            return redirect('core:dashboard')
    else:
        raise PermissionDenied

def demo_login(request):
    demo.reset_demouser() # Reset the demo data anytime someone tries to access it
    auth_user = authenticate(username=demo.USERNAME, password=demo.PASSWORD)
    login(request, auth_user)
    return redirect('core:dashboard')

def register(request):
    username = request.POST.get('username', '').strip()
    if username == '' or User.objects.filter(username=username).exists():
        messages.info(request, 'invalid_username')
        return redirect('core:intro')

    if 'captcha' not in request.POST:
        # Username accepted, now give nocaptcha input
        context = {'form': CaptchaForm(), 'username': username}
        return render(request, 'register.html', context)
    else:
        # nocaptcha posted; validate and create user
        form = CaptchaForm(request.POST)
        if not form.is_valid():
            messages.info(request, 'invalid_captcha')
            return redirect('core:intro')
        else:
            password = request.POST.get('password', '').strip()
            User.objects.create_user(username=username, password=password)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('core:dashboard')

@login_required
def dashboard(request):
    watches = request.user.watches.select_related('series').prefetch_related('series__episodes').all()
    active_watches = [s for s in watches if s.status == 'active']
    default_watches = [s for s in watches if s.status == 'default']
    archived_watches = [s for s in watches if s.status == 'archived']
    context = {
        'active_watches': active_watches,
        'default_watches': default_watches,
        'archived_watches': archived_watches,
    }
    return render(request, 'home/dashboard.html', context)

@login_required
def account(request):
    if request.method == 'GET':
        return render(request, 'home/account.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if request.user.username == demo.USERNAME and username != demo.USERNAME:
            messages.info(request, 'cannot_change_demo_username')
            return redirect('core:account')

        if username == '' or User.objects.filter(username=username).exclude(id=request.user.id).exists():
            messages.info(request, 'invalid_username')
            return redirect('core:account')

        request.user.username = username
        request.user.set_password(password)
        request.user.save()
        messages.info(request, 'account_updated')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('core:account')
    else:
        raise PermissionDenied

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
    try:
        watching = Watching.objects.select_related(
            'series',
        ).prefetch_related(
            'series__episodes',
        ).get(id=watching_id, user=request.user)
        context = {'watching': watching}
        return render(request, 'home/series.html', context)
    except Watching.DoesNotExist:
        return redirect('core:dashboard')

@login_required
def watching_seen(request, watching_id):
    try:
        watching = Watching.objects.get(id=watching_id, user=request.user)
        if 'increment' in request.GET:
            watching.move_seen('next')
            return redirect('core:dashboard')
        elif 'decrement' in request.GET:
            watching.move_seen('previous')
            return redirect('core:dashboard')
        elif 'last-seen' in request.POST:
            try:
                last_seen = request.POST['last-seen'].strip()
                if last_seen != '':
                    season, episode = last_seen.split('x')
                    last_seen = "%sx%02d" % (int(season), int(episode))
                watching.last_seen = last_seen
                watching.save()
            except ValueError:
                messages.info(request, 'invalid_seen')
            return redirect('core:watching', watching.id)
        else:
            return redirect('core:dashboard')
    except Watching.DoesNotExist:
        return redirect('core:dashboard')

@login_required
def watching_status(request, watching_id):
    try:
        status = request.GET.get('status', '')
        if status not in [s[0] for s in Watching.STATUS_CHOICES]:
            raise PermissionDenied

        watching = Watching.objects.get(id=watching_id, user=request.user)
        watching.status = status
        watching.save()
        return redirect('core:dashboard')
    except Watching.DoesNotExist:
        return redirect('core:dashboard')

@login_required
def watching_stop(request, watching_id):
    try:
        Watching.objects.get(id=watching_id, user=request.user).delete()
        return redirect('core:dashboard')
    except Watching.DoesNotExist:
        return redirect('core:dashboard')
