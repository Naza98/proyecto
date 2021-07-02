from django.contrib import admin
from .models import Provincia, Localidad, Barrio

class ProvinciaAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nombre_provincia'
    ]


class LocalidadAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nombre_localidad'
    ]

class BarrioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nombre_barrio'
    ]

admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(Localidad, LocalidadAdmin)
admin.site.register(Barrio, BarrioAdmin)


