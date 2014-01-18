# encoding: utf-8
from django.core.management.base import BaseCommand

from core import tvdb
from core.models import Show

class Command(BaseCommand):
    args = u''
    help = u"Sync all shows"

    def handle(self, *args, **options):
        for show in Show.objects.all():
            tvdb.create_or_update_show(show.tvdbid)
