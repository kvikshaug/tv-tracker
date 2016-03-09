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
    # TODO: Remove stale episode objects
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
        'status': series_data.status,
        'banner': series_data.banner,
        'first_aired': series_data.first_aired,
        'imdb': series_data.imdb,
    })

    for episode_data in series_data.episodes:
        episode, created = series.episodes.get_or_create(season=episode_data.season, episode=episode_data.episode)
        episode.air_date = episode_data.air_date
        episode.save()

    return series
