from django.urls import path, include

from .views import ProveedorView,ProveedorNew, ProveedorEdit, \
    proveedorInactivar, ProveedorDetail, \
    ComprasView, compras, CompraDetDelete,eliminar_detalle

from .reportes import reporte_compras, imprimir_compra, imprimir_compras_list

urlpatterns = [
    path('proveedores/',ProveedorView.as_view(), name="proveedor_list"),
    path('proveedores/new',ProveedorNew.as_view(), name="proveedor_new"),
    path('proveedores/edit/<int:pk>',ProveedorEdit.as_view(), name="proveedor_edit"),
    path('proveedores/inactivar/<int:id>',proveedorInactivar, name="proveedor_inactivar"),
    path('proveedores/detalle/<int:pk>', ProveedorDetail.as_view(), name='proveedor_detalle'),

    path('compras/',ComprasView.as_view(), name="compras_list"),
    path('compras/new',compras, name="compras_new"),
    path('compras/edit/<int:compra_id>',compras, name="compras_edit"),
    path('compras/<int:compra_id>/delete/<int:pk>',CompraDetDelete.as_view(), name="compras_del"),
    path('compras/eliminar-detalle/<int:id>',eliminar_detalle,name="eliminar_detalle"),

    path('compras/listado', reporte_compras, name='compras_print_all'),
    path('compras/imprimir-todas/<str:f1>/<str:f2>',imprimir_compras_list, name="compras_imprimir_all"),
    path('compras/<int:compra_id>/imprimir', imprimir_compra,name="compras_print_one"),
]