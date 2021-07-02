from django.urls import path
from .views import ProvinciaView, ProvinicaNew, ProvinciaEdit, \
    LocalidadNew, LocalidadView, LocalidadEdit

urlpatterns = [
    path('provincias/',ProvinciaView.as_view(), name='provincia_list'),
    path('provincias/new',ProvinicaNew.as_view(), name='provincia_new'),
    path('provincias/edit/<int:pk>',ProvinciaEdit.as_view(), name='provincia_edit'),

    path('localidades/',LocalidadView.as_view(), name='localidad_list'),
    path('localidades/new',LocalidadNew.as_view(), name='localidad_new'),
    path('localidades/edit/<int:pk>',LocalidadEdit.as_view(), name='localidad_edit')
]
