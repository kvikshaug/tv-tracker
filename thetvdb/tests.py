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

    def get_series_all_6_seasons(self, url):
        with open('test/data/series_152831_all_6_seasons.zip', 'rb') as f:
            response = MockRequestsResponse(f.read())
        return response

    def get_series_all_7_seasons(self, url):
        with open('test/data/series_152831_all_7_seasons.zip', 'rb') as f:
            response = MockRequestsResponse(f.read())
        return response

    #
    # Tests
    #

    def test_create_series(self):
        with Replace('requests.get', self.get_series_all_6_seasons):
            tvdb.create_or_update_series(152831)
            series = Series.objects.get(tvdbid=152831)
            self.assertEqual(series.name, 'Adventure Time')
            self.assertEqual(series.seasons.count(), 6)

    def test_update_series(self):
        with Replace('requests.get', self.get_series_all_6_seasons):
            tvdb.create_or_update_series(152831)
            created_series = Series.objects.get(tvdbid=152831)
            self.assertEqual(created_series.seasons.count(), 6)

        with Replace('requests.get', self.get_series_all_7_seasons):
            tvdb.create_or_update_series(152831)
            updated_series = Series.objects.get(tvdbid=152831)
            self.assertEqual(updated_series.name, 'Adventure Time')
            self.assertEqual(updated_series.seasons.count(), 7)
            self.assertEqual(created_series.id, updated_series.id)
            self.assertEqual(Series.objects.count(), 1)
