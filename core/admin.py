from django.contrib import admin

from .models import LastUpdate, Series, Episode

admin.site.register(LastUpdate)
admin.site.register(Series)
admin.site.register(Episode)
