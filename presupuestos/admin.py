from django.contrib import admin
from .models import Presupuesto

class PresAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'producto',
        'cliente',
        'precio_unitario',
        'cantidad',
        'total',
        'plazo'
    ]


admin.site.register(Presupuesto, PresAdmin)
