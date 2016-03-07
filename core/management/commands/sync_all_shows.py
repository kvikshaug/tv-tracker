from datetime import datetime

from django.core.management.base import BaseCommand

from core import tvdb
from core.models import LastUpdate, Series

class Command(BaseCommand):
    args = ""
    help = "Sync all series"

    def handle(self, *args, **options):
        for series in Series.objects.all():
            tvdb.create_or_update_series(series.tvdbid)
        last_update = LastUpdate.objects.get()
        last_update.date = datetime.now()
        last_update.save()
