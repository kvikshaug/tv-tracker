from django.test import TestCase

from testfixtures import Replace

from core.models import Series
from thetvdb import tvdb

class MockRequestsResponse:
    def __init__(self, content):
        self.content = content

class TheTVDBTestCase(TestCase):
    #
    # Mock methods
    #

    def get_series_all(self, url):
        with open('test/data/series_152831_all.zip', 'rb') as f:
            response = MockRequestsResponse(f.read())
        return response

    #
    # Tests
    #

    def test_create_series(self):
        with Replace('requests.get', self.get_series_all):
            tvdb.create_or_update_series(152831)
            series = Series.objects.get(tvdbid=152831)
            self.assertEqual(series.name, 'Adventure Time')
            self.assertEqual(series.seasons.count(), 7)
