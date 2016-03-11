from django.contrib import admin

from .models import LastUpdate, Watching, Series, Episode

admin.site.register(LastUpdate)
admin.site.register(Watching)
admin.site.register(Series)
admin.site.register(Episode)
