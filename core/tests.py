from datetime import datetime

from django.test import TestCase, Client

from core.models import LastUpdate

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        LastUpdate.objects.create(datetime=datetime(2016, 1, 1, 12, 0, 0))

    def test_get_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
