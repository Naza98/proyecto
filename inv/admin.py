from django.contrib import admin

from .models import Categoria, SubCategoria, Marca, Producto, \
    TipoMovimiento, Movimiento, HistorialPreciosVenta

class ProductoAdmin(admin.ModelAdmin):
    list_display = [
        'codigo',
        'nombre_producto',
        'marca',
        'descripcion',
        'precio',
        'existencia',
        'ultima_compra',
        'subcategoria',
        'foto',
    ]

class TipoMovimientoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'descripcion'
    ]


class MovimientoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'producto',
        'tipo_movimiento',
        'fecha',
        'cantidad'
    ]

class HistorialPreciosVentaAdmin(admin.ModelAdmin):
    list_display = [
        'producto',
        'fecha_modificacion',
        'precio',
    ]



admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(Marca)
admin.site.register(TipoMovimiento, TipoMovimientoAdmin)
admin.site.register(Movimiento,MovimientoAdmin)
admin.site.register(HistorialPreciosVenta,HistorialPreciosVentaAdmin)

