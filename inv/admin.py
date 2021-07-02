from django.contrib import admin

from .models import Categoria, SubCategoria, Marca, Producto, \
    TipoMovimiento, Movimiento, HistorialPreciosVenta, Motivo


class CategoriaAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'descripcion'
    ]

class SubCategoriaAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'descripcion'
    ]

class MarcaAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'descripcion'
    ]

class ProductoAdmin(admin.ModelAdmin):
    list_display = [
        'codigo',
        'codigo_barra',
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

class MotivoAdmin(admin.ModelAdmin):
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
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(SubCategoria, SubCategoriaAdmin)
admin.site.register(Marca, MarcaAdmin)
admin.site.register(TipoMovimiento, TipoMovimientoAdmin)
admin.site.register(Motivo, MotivoAdmin)
admin.site.register(Movimiento,MovimientoAdmin)
admin.site.register(HistorialPreciosVenta,HistorialPreciosVentaAdmin)

