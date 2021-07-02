from django.urls import path, include
from django.conf.urls import url

from presupuestos import views

from .reportes import imprimir_presupuesto, imprimir_presupuesto_list

urlpatterns = [
    path('pre/', views.presupuestos_view, name='presupuestos_view'),
    path('pre/getPrecio/', views.getPrecio, name='getPrecio'),    
    path('pre/eliminar/<int:id>', views.eliminar, name='eliminar_presupuesto'), 
    path('pre/<int:presupuesto_id>/imprimir', imprimir_presupuesto, name='presupuesto_print_one'),
    path('pre/imprimir-todos/<str:f1>/<str:f2>',imprimir_presupuesto_list, name="presupuesto_imprimir_all"),
]
