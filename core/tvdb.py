from django.conf import settings

from lxml import etree
from datetime import datetime
from io import BytesIO
import zipfile
import requests

from core.models import Series

API_PATH = "http://thetvdb.com/api"

#
# Models
#

class SeriesSearchResult():
    def __init__(self, id, name, overview, banner, first_aired, imdb):
        self.id = id
        self.name = name
        self.overview = overview
        self.banner = banner
        self.first_aired = first_aired
        self.imdb = imdb

class TVDBSeries():
    def __init__(self, tvdbid, name, overview, status, banner, first_aired, imdb):
        self.tvdbid = tvdbid
        self.name = name
        self.overview = overview
        self.status = status
        self.banner = banner
        self.first_aired = first_aired
        self.imdb = imdb
        self.episodes = []

    def add_episode(self, season):
        self.episodes.append(season)

class TVDBEpisode():
    def __init__(self, season, number, first_aired):
        self.season = season
        self.number = number
        self.first_aired = first_aired

#
# Available methods
#

def search_for_series(query):
    content = requests.get("%s/GetSeries.php?seriesname=%s" % (API_PATH, query)).content
    xml = etree.fromstring(content)
    return [parse_search_result(series_xml) for series_xml in xml.findall("Series")]

def create_or_update_show(tvdbid):
    # TODO: Remove stale episode objects
    zipped = requests.get('%s/%s/series/%s/all/en.zip' % (API_PATH, settings.TVDB_API_KEY, tvdbid)).content
    content = zipfile.ZipFile(BytesIO(zipped)).read('en.xml')
    xml = etree.fromstring(content)

    series_data = parse_series(xml)

    show, created = Series.objects.update_or_create(tvdbid=series_data.tvdbid, defaults={
        'name': series_data.name,
        'status': series_data.status,
        'banner': series_data.banner,
        'first_aired': series_data.first_aired,
        'imdb': series_data.imdb,
    })

    for episode_data in series_data.episodes:
        season, created = show.seasons.get_or_create(number=episode_data.season)
        episode, created = season.episodes.get_or_create(number=episode_data.number)
        episode.air_date = episode_data.first_aired
        episode.save()

    return show


#
# Parsing and utilities
#

def try_field(xml, field_name, default=''):
    field = xml.find(field_name)
    if field is not None:
        return field.text
    else:
        return default

def parse_search_result(xml):
    # Fields we require (i.e. throw exception if missing)
    id = xml.find('seriesid').text
    name = xml.find('SeriesName').text

    # Nice-to-have fields
    overview = try_field(xml, 'Overview')
    banner = try_field(xml, 'banner')
    first_aired = try_field(xml, 'FirstAired')
    imdb = try_field(xml, 'IMDB_ID')

    try:
        first_aired = datetime.strptime(first_aired, "%Y-%m-%d")
    except (ValueError, TypeError):
        first_aired = None

    return SeriesSearchResult(id, name, overview, banner, first_aired, imdb)

def parse_series(xml):
    series = xml.find("Series")
    tvdbid = try_field(series, "id")
    name = try_field(series, "SeriesName")
    overview = try_field(series, "Overview")
    status = try_field(series, "Status")
    banner = try_field(series, "banner")
    first_aired = try_field(series, "FirstAired")
    imdb = try_field(series, "IMDB_ID")

    try:
        first_aired = datetime.strptime(first_aired, "%Y-%m-%d")
    except (ValueError, TypeError):
        first_aired = None

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

        series.add_episode(TVDBEpisode(
            season=season,
            number=number,
            first_aired=first_aired,
        ))

    return series
