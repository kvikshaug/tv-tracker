from datetime import date

from django.template import Library

register = Library()

@register.filter
def status_class(episode, watching):
    """episode css status class shortcut"""
    if episode.air_date is None or episode.air_date > date.today():
        return 'unaired'
    else:
        if not watching.has_last_seen():
            return 'available'

        seen_season, seen_episode = watching.get_last_seen()
        if episode.season > seen_season:
            return 'available'
        elif episode.season == seen_season:
            if episode.episode > seen_episode:
                return 'available'
            else:
                return 'seen'
        else:
            return 'seen'
