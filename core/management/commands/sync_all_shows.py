# encoding: utf-8
from datetime import datetime

from django.core.management.base import BaseCommand

from core import tvdb
from core.models import LastUpdate, Show

class Command(BaseCommand):
    args = u''
    help = u"Sync all shows"

    def handle(self, *args, **options):
        for show in Show.objects.all():
            tvdb.create_or_update_show(show.tvdbid)
        last_update = LastUpdate.objects.get()
        last_update.date = datetime.now()
        last_update.save()
