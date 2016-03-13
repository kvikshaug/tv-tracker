from datetime import date

from django.template import Library

from core.models import Watching

register = Library()

@register.filter
def watching(user, tvdbid):
    """If the user is watching the given tvdbid, returns the Wathing object, otherwise None"""
    try:
        return Watching.objects.get(user=user, series__tvdbid=tvdbid)
    except Watching.DoesNotExist:
        return None
