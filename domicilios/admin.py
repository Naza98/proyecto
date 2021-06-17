from django.contrib import admin
from .models import Provincia, Localidad, Barrio, Domicilio

admin.site.register(Provincia)
admin.site.register(Localidad)
admin.site.register(Barrio)
admin.site.register(Domicilio)


