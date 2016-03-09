from django.conf import settings

from datetime import datetime
from io import BytesIO
from xml.etree import ElementTree
import zipfile

import requests

from .models import SeriesSearchResult, Series as TVDBSeries, Episode
from core.models import Series

def search_for_series(query):
    content = requests.get("%s/GetSeries.php?seriesname=%s" % (settings.TVDB_API_ENDPOINT, query)).content
    xml = ElementTree.fromstring(content)
    return [parse_search_result(series_xml) for series_xml in xml.findall("Series")]

def create_or_update_series(tvdbid):
    # TODO: Remove stale episode objects
    zipped = requests.get("%s/%s/series/%s/all/en.zip" % (
        settings.TVDB_API_ENDPOINT,
        settings.TVDB_API_KEY,
        tvdbid,
    )).content
    content = zipfile.ZipFile(BytesIO(zipped)).read("en.xml")
    xml = ElementTree.fromstring(content)

    series_data = parse_series(xml)

    series, created = Series.objects.update_or_create(tvdbid=series_data.tvdbid, defaults={
        'name': series_data.name,
        'status': series_data.status,
        'banner': series_data.banner,
        'first_aired': series_data.first_aired,
        'imdb': series_data.imdb,
    })

    for episode_data in series_data.episodes:
        season, created = series.seasons.get_or_create(number=episode_data.season)
        episode, created = season.episodes.get_or_create(number=episode_data.number)
        episode.air_date = episode_data.first_aired
        episode.save()

    return series


#
# Parsing and utilities
#

def parse_search_result(xml):
    # Required fields (i.e. throw exception if missing)
    id = xml.find('seriesid').text
    name = xml.find('SeriesName').text

    # Optional fields
    overview = xml.findtext('Overview', default='')
    banner = xml.findtext('banner', default='')
    try:
        first_aired = datetime.strptime(xml.findtext('FirstAired', default=''), "%Y-%m-%d")
    except ValueError:
        first_aired = None
    imdb = xml.findtext('IMDB_ID', default='')

    return SeriesSearchResult(id, name, overview, banner, first_aired, imdb)

def parse_series(xml):
    series = xml.find("Series")
    tvdbid = series.findtext("id", default='')
    name = series.findtext("SeriesName", default='')
    overview = series.findtext("Overview", default='')
    status = series.findtext("Status", default='')
    banner = series.findtext("banner", default='')
    try:
        first_aired = datetime.strptime(series.findtext("FirstAired", default=''), "%Y-%m-%d")
    except ValueError:
        first_aired = None
    imdb = series.findtext("IMDB_ID", default='')

    series = TVDBSeries(
        tvdbid=tvdbid,
        name=name,
        overview=overview,
        status=status,
        banner=banner,
        first_aired=first_aired,
        imdb=imdb,
    )

    for e in xml.findall("Episode"):
        season = try_field(e, "SeasonNumber")
        if season == '0':
            # Ignore specials for now
            continue

        number = try_field(e, "EpisodeNumber")
        first_aired = try_field(e, "FirstAired")

        try:
            first_aired = datetime.strptime(first_aired, "%Y-%m-%d")
        except (ValueError, TypeError):
            first_aired = None

        series.add_episode(Episode(
            season=season,
            number=number,
            first_aired=first_aired,
        ))

    return series
