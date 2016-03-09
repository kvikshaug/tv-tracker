from django.test import TestCase

from testfixtures import Replace

from core.models import Series, Episode
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
            self.assertEqual(len(series.episodes_by_season()), 6)

    def test_update_series(self):
        with Replace('requests.get', self.get_series_all_6_seasons):
            tvdb.create_or_update_series(152831)
            created_series = Series.objects.get(tvdbid=152831)
            self.assertEqual(len(created_series.episodes_by_season()), 6)

        with Replace('requests.get', self.get_series_all_7_seasons):
            tvdb.create_or_update_series(152831)
            updated_series = Series.objects.get(tvdbid=152831)
            self.assertEqual(updated_series.name, 'Adventure Time')
            self.assertEqual(len(updated_series.episodes_by_season()), 7)
            self.assertEqual(created_series.id, updated_series.id)
            self.assertEqual(Series.objects.count(), 1)

    def test_remove_stale_episodes(self):
        series = Series.objects.create(tvdbid=152831)
        stale_episode = Episode.objects.create(series=series, season=8, episode=1)
        self.assertEqual(series.episodes.filter(season=8).exists(), True)

        with Replace('requests.get', self.get_series_all_7_seasons):
            tvdb.create_or_update_series(series.tvdbid)

        self.assertEqual(series.episodes.filter(season=8).exists(), False)
