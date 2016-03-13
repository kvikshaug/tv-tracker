from datetime import date

from django.template import Library

register = Library()

@register.filter
def status_class(episode, watching):
    """episode css status class shortcut"""
    # Seen is seen, regardless of air date
    if watching.has_last_seen():
        seen_season, seen_episode = watching.get_last_seen()
        if seen_season > episode.season or (
                seen_season == episode.season and
                seen_episode >= episode.episode):
            return 'seen'

    # Not seen, so it's either aired or not
    if episode.air_date is not None and episode.air_date <= date.today():
        return 'available'
    else:
        return 'unaired'
