from lxml import etree
from datetime import datetime
import requests

API_PATH = "http://thetvdb.com/api"

class SeriesSearch():
    def __init__(self, id, name, first_aired, imdb):
        self.id = id
        self.name = name
        self.first_aired = first_aired
        self.imdb = imdb

def search_series(query):
    html = requests.get("%s/GetSeries.php?seriesname=%s" % (API_PATH, query)).content
    xml = etree.fromstring(html)

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
        o = SeriesSearch(id, name, first_aired, imdb)
        results.append(o)
    return results
