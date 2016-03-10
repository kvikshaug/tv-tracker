from django.conf import settings

from io import BytesIO
from xml.etree import ElementTree
import zipfile

import requests

from .models import SeriesSearchResult, Series as TVDBSeries
from core.models import Series

def search_for_series(query):
    content = requests.get("%s/GetSeries.php?seriesname=%s" % (settings.TVDB_API_ENDPOINT, query)).content
    xml = ElementTree.fromstring(content)
    return [SeriesSearchResult.from_xml(series_xml) for series_xml in xml.findall("Series")]

def create_or_update_series(tvdbid):
    zipped = requests.get("%s/%s/series/%s/all/en.zip" % (
        settings.TVDB_API_ENDPOINT,
        settings.TVDB_API_KEY,
        tvdbid,
    )).content
    content = zipfile.ZipFile(BytesIO(zipped)).read("en.xml")
    xml = ElementTree.fromstring(content)

    series_data = TVDBSeries.from_xml(xml)

    series, created = Series.objects.update_or_create(tvdbid=series_data.tvdbid, defaults={
        'name': series_data.name,
        'description': series_data.description,
        'status': series_data.status,
        'banner': series_data.banner,
        'poster': series_data.poster,
        'first_aired': series_data.first_aired,
        'imdb': series_data.imdb,
    })
    episodes = series.episodes.all()

    # Delete removed episodes
    for episode in episodes:
        if not any([e.season == episode.season and e.episode == episode.episode for e in series_data.episodes]):
            episode.delete()

    # Create new and update existing episodes
    for episode_data in series_data.episodes:
        episode_matches = [e for e in episodes if e.season == episode_data.season and e.episode == episode_data.episode]
        if len(episode_matches) == 0:
            # Episode doesn't exist, create it
            series.episodes.create(
                season=episode_data.season,
                episode=episode_data.episode,
                air_date=episode_data.air_date,
            )
        elif len(episode_matches) == 1:
            # Episode exist, update it only if it differs
            episode = episode_matches[0]
            if episode.air_date != episode_data.air_date:
                episode.air_date = episode_data.air_date
                episode.save()
        else:
            raise Exception("Invalid state; episode '%s' is duplicated despite UNIQUE constraint" % episode_matches[0])

    return series
