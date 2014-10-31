from core.models import LastUpdate

def last_update(request):
    return {'last_update': LastUpdate.objects.get().date}
