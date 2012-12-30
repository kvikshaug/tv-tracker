from django.conf import settings

from lxml import etree
from datetime import datetime
from cStringIO import StringIO
import zipfile
import requests

from app.models import Show, Season, Episode

API_PATH = "http://thetvdb.com/api"

class ShowSearched():
    def __init__(self, id, name, first_aired, imdb):
        self.id = id
        self.name = name
        self.first_aired = first_aired
        self.imdb = imdb

def search_series(query):
    content = requests.get("%s/GetSeries.php?seriesname=%s" % (API_PATH, query)).content
    xml = etree.fromstring(content)

    # Relatively simple parsing, I bet some kind of error will appear here for some obscure search sometime.
    results = []
    for s in xml.findall("Series"):
        id = s.find('seriesid').text
        name = s.find('SeriesName').text
        first_aired = s.find('FirstAired')
        if first_aired is not None:
            first_aired = datetime.strptime(first_aired.text, "%Y-%m-%d")
        imdb = s.find('IMDB_ID')
        if imdb is not None:
            imdb = imdb.text
        results.append(ShowSearched(id, name, first_aired, imdb))
    return results

def add_show(id):
    zipped = requests.get('%s/%s/series/%s/all/en.zip' % (API_PATH, settings.TVDB_API_KEY, id)).content
    content = zipfile.ZipFile(StringIO(zipped)).read('en.xml')
    xml = etree.fromstring(content)

    series = xml.find("Series")
    name = series.find("SeriesName").text
    banner = series.find("banner")
    if banner is None:
        banner = ''
    else:
        banner = banner.text
    status = series.find("Status").text
    first_aired = series.find("FirstAired")
    if first_aired is not None:
        first_aired = datetime.strptime(first_aired.text, "%Y-%m-%d")
    imdb = series.find("IMDB_ID")
    if imdb is None:
        imdb = ''
    else:
        imdb = imdb.text

    show = Show(
        tvdbid=id,
        name=name,
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
        if not Episode.objects.filter(number=episode_number, season=season).exists():
            episode = Episode(
                number=episode_number,
                season=season)
            episode.save()

    return show
