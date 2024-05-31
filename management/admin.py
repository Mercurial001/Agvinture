from django.contrib import admin
from .models import Trees
from .models import Lot
from .models import Section
from .models import Geolocation
from .models import PlantedStatus
from .models import Coordinates


class CoordinatesAdmin(admin.ModelAdmin):
    list_display = ('section', 'point', 'long', 'lat')


class PlantedStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)


class SectionAdmin(admin.ModelAdmin):
    list_display = ('name',)


class LotAdmin(admin.ModelAdmin):
    list_display = ('name',)


class TreesAdmin(admin.ModelAdmin):
    list_display = ('name',)


class GeolocationAdmin(admin.ModelAdmin):
    list_display = ('section', 'lot', 'tree', 'lat', 'long')


admin.site.register(Coordinates, CoordinatesAdmin)
admin.site.register(PlantedStatus, PlantedStatusAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Lot, LotAdmin)
admin.site.register(Trees, TreesAdmin)
admin.site.register(Geolocation, GeolocationAdmin)
