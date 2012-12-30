from lxml import etree
import requests

API_PATH = "http://thetvdb.com/api"

def search_series(query):
    html = requests.get("%s/GetSeries.php?seriesname=%s" % (API_PATH, query)).content
    xml = etree.fromstring(html)
    print(xml)
    return ['foo', 'bar']
