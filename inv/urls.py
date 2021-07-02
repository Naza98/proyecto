from django.urls import path

from .views import ActualizarPrecioTemplateView, CategoriaView, CategoriaNew, CategoriaEdit, \
    categoria_inactivar, \
    SubCategoriaView, SubCategoriaNew, SubCategoriaEdit, subcategoria_inactivar, \
    MarcaView, MarcaNew, MarcaEdit, marca_inactivar, \
    ProductoView, ProductoEdit, ProductoNew, producto_inactivar, ProductoDetail, \
    HistorialPreciosProductos, MovimientoView, MovimientoNew, MovimientoEdit
    

from .reportes import historial_precios_productos, imprimir_movimientos, movimiento_unico  

urlpatterns = [
    path('categorias/',CategoriaView.as_view(), name='categoria_list'),
    path('categorias/new',CategoriaNew.as_view(), name='categoria_new'),
    path('categorias/edit/<int:pk>',CategoriaEdit.as_view(), name='categoria_edit'),
    path('categorias/inactivar/<int:id>',categoria_inactivar, name="categoria_inactivar"),
    #path('categorias/delete/<int:pk>',CategoriaDel.as_view(), name='categoria_del'),

    path('subcategorias/',SubCategoriaView.as_view(), name='subcategoria_list'),
    path('subcategorias/new',SubCategoriaNew.as_view(), name='subcategoria_new'),
    path('subcategorias/edit/<int:pk>',SubCategoriaEdit.as_view(), name='subcategoria_edit'),
    path('subcategorias/inactivar/<int:id>',subcategoria_inactivar, name="subcategoria_inactivar"),
    #path('subcategorias/delete/<int:pk>',SubCategoriaDel.as_view(), name='subcategoria_del'),

    path('marcas/',MarcaView.as_view(), name="marca_list"),
    path('marcas/new',MarcaNew.as_view(), name="marca_new"),
    path('marcas/edit/<int:pk>',MarcaEdit.as_view(), name="marca_edit"),
    path('marcas/inactivar/<int:id>',marca_inactivar, name="marca_inactivar"),

    path('productos/',ProductoView.as_view(), name="producto_list"),
    path('productos/new',ProductoNew.as_view(), name="producto_new"),
    path('productos/edit/<int:pk>',ProductoEdit.as_view(), name="producto_edit"),
    path('productos/inactivar/<int:id>',producto_inactivar, name="producto_inactivar"),
    path('productos/detalle/<int:pk>', ProductoDetail.as_view(), name='producto_detalle'),
    path('productos/historial_precios',HistorialPreciosProductos.as_view(), name="historial_precios"),
    path('productos/historial_precios_print_all', historial_precios_productos, name='historial_precios_print_all'),
    #para actualizar precios 
    path('productos/actualizar_precios',  ActualizarPrecioTemplateView.as_view(), name='actualizar-precios'), 

    #Movimientos
    path('movimientos/',MovimientoView.as_view(), name="movimiento_list"),
    path('movimientos/new',MovimientoNew.as_view(), name="movimiento_new"),
    path('movimientos/edit/<int:pk>',MovimientoEdit.as_view(), name="movimiento_edit"),
    path('movimientos/imprimir_movimientos', imprimir_movimientos, name='imprimir_movimientos'),
    path('movimientos/<int:movimiento_id>/imprimir', movimiento_unico, name='movimiento_print_one'),
    
    #path('um/',UMView.as_view(), name="um_list"),
    #path('um/new',UMNew.as_view(), name="um_new"),
    #path('um/edit/<int:pk>',UMEdit.as_view(), name="um_edit"),
    #path('um/inactivar/<int:id>',um_inactivar, name="um_inactivar"),
    
    
]