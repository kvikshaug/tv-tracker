from django.conf import settings

from lxml import etree
from datetime import datetime
from io import StringIO
import zipfile
import requests

from core.models import Show, Season, Episode

API_PATH = "http://thetvdb.com/api"

#
# Models
#

class SeriesResult():
    def __init__(self, id, name, overview, banner, first_aired, imdb):
        self.id = id
        self.name = name
        self.overview = overview
        self.banner = banner
        self.first_aired = first_aired
        self.imdb = imdb

#
# Utilities
#

def try_field(xml, field_name, default=''):
    field = xml.find(field_name)
    if field is not None:
        return field.text
    else:
        return default

#
# Available methods
#

def search_for_series(query):
    content = requests.get("%s/GetSeries.php?seriesname=%s" % (API_PATH, query)).content
    xml = etree.fromstring(content)
    return [parse_search_result(series_xml) for series_xml in xml.findall("Series")]

def parse_search_result(xml):
    # Fields we require (i.e. throw exception if missing)
    id = xml.find('seriesid').text
    name = xml.find('SeriesName').text

    # Nice-to-have fields
    overview = try_field(xml, 'Overview')
    banner = try_field(xml, 'banner')
    first_aired = try_field(xml, 'FirstAired')
    imdb = try_field(xml, 'IMDB_ID')

    # Try to parse the first_aired date
    try:
        first_aired = datetime.strptime(first_aired, "%Y-%m-%d")
    except (ValueError, TypeError):
        first_aired = None

    return SeriesResult(id, name, overview, banner, first_aired, imdb)

def add_show(id):
    zipped = requests.get('%s/%s/series/%s/all/en.zip' % (API_PATH, settings.TVDB_API_KEY, id)).content
    content = zipfile.ZipFile(StringIO(zipped)).read('en.xml')
    xml = etree.fromstring(content)

    series = xml.find("Series")
    name = series.find("SeriesName").text
    banner = series.find("banner").text
    if banner is None:
        banner = ''
    else:
        banner = banner
    status = series.find("Status").text
    first_aired = series.find("FirstAired").text
    if first_aired is not None:
        first_aired = datetime.strptime(first_aired, "%Y-%m-%d")
    imdb = series.find("IMDB_ID").text
    if imdb is None:
        imdb = ''

    try:
        show = Show.objects.get(tvdbid=id)
        show.tvdbid = id
        show.name = name
        show.status = status
        show.banner = banner
        show.first_aired = first_aired
        show.imdb = imdb
    except Show.DoesNotExist:
        show = Show(
            tvdbid=id,
            name=name,
            status=status,
            banner=banner,
            first_aired=first_aired,
            imdb=imdb)

    show.save()

    for e in xml.findall("Episode"):
        season_number = e.find("SeasonNumber").text
        if season_number == '0':
            # Ignore specials for now
            continue

        try:
            season = Season.objects.get(show=show, number=season_number)
        except Season.DoesNotExist:
            season = Season(
                number=season_number,
                show=show)
            season.save()

        episode_number = e.find("EpisodeNumber").text
        first_aired = e.find("FirstAired").text
        if first_aired is not None:
            first_aired = datetime.strptime(first_aired, "%Y-%m-%d")
        try:
            episode = Episode.objects.get(number=episode_number, season=season)
            episode.air_date = first_aired
        except Episode.DoesNotExist:
            episode = Episode(
                number=episode_number,
                air_date=first_aired,
                season=season)
        episode.save()

    return show
