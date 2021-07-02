from django.contrib import admin

from .models import Cliente, FacturaEnc, FacturaDet, FormaPago, TipoFactura

class ClienteAdmin(admin.ModelAdmin):
    list_display = [
        'nombres',
        'apellidos',
        'numero_dni',
    ]

class TipoFacturaAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'descripcion'
    ]    

class FormaPagoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'descripcion'
    ]    


class FacturaEncAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'cliente',
        'fecha',
        'sub_total',
        'descuento',
        'total',
        'forma_pago',
        'tipo_factura'
    ]

class FacturaDetAdmin(admin.ModelAdmin):
    list_display = [
        'factura',
        'producto',
        'cantidad',
        'precio',
        'total'
    ]


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(FacturaEnc, FacturaEncAdmin)
admin.site.register(FacturaDet, FacturaDetAdmin)
admin.site.register(FormaPago, FormaPagoAdmin)
admin.site.register(TipoFactura, TipoFacturaAdmin)

