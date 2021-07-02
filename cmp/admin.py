from django.contrib import admin
from .models import ComprasDet, ComprasEnc, Proveedor


class ProveedorAdmin(admin.ModelAdmin):
    list_display = [
        'descripcion',
        'contacto',
        'telefono'
    ]

class ComprasEncAdmin(admin.ModelAdmin):
    list_display = [
        'fecha_compra',
        'observacion',
        'no_factura',
        'fecha_factura',
        'sub_total',
        'descuento',
        'total'
    ]

class ComprasDetAdmin(admin.ModelAdmin):
    list_display = [
        'compra',
        'producto',
        'cantidad',
        'precio_prv',
        'total'
    ]



admin.site.register(ComprasEnc, ComprasEncAdmin)
admin.site.register(ComprasDet, ComprasDetAdmin)
admin.site.register(Proveedor, ProveedorAdmin)