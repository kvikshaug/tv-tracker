from django.core.management.base import BaseCommand

from core.demo import reset_demouser

class Command(BaseCommand):
    def handle(self, *args, **options):
        reset_demouser()
