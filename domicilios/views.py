from django.urls.base import reverse_lazy
from django.views import generic
from bases.views import SinPrivilegios
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView

from .models import Provincia, Localidad, Barrio 
from .forms import ProvinciaForm, LocalidadForm, BarrioForm


class ProvinciaView(SinPrivilegios, generic.ListView):
    permission_required = "domicilios.view_provincia" #permiso para acceder al la lista 
    model = Provincia
    queryset = Provincia.objects.all()
    obj = queryset
    template_name = "provincias/provincia_list.html"
    context_object_name = "obj"

class ProvinicaNew(SuccessMessageMixin,SinPrivilegios,\
    generic.CreateView):
    permission_required="domicilios.add_provincia"
    model=Provincia
    template_name="provincias/provincia_form.html"
    context_object_name = "obj"
    form_class=ProvinciaForm
    success_url=reverse_lazy("dom:provincia_list")
    success_message="Provincia Creada Satisfactoriamente"


class ProvinciaEdit(SuccessMessageMixin,SinPrivilegios, \
    generic.UpdateView):
    permission_required="domicilios.change_provincia"
    model=Provincia
    template_name="provincias/provincia_form.html"
    context_object_name = "obj"
    form_class=ProvinciaForm
    success_url=reverse_lazy("dom:provincia_list")
    success_message="Provincia Actualizada Satisfactoriamente"



class LocalidadView(SinPrivilegios, generic.ListView):
    permission_required = "domicilios.view_localidad" #permiso para acceder al la lista 
    model = Localidad
    queryset = Localidad.objects.all()
    obj = queryset
    template_name = "localidades/localidad_list.html"
    context_object_name = "obj"


class LocalidadNew(SuccessMessageMixin,SinPrivilegios, generic.CreateView):
    model=Localidad
    template_name="localidades/localidad_form.html"
    context_object_name = "obj"
    form_class=LocalidadForm
    success_url=reverse_lazy("dom:localidad_list")
    success_message="Localidad Creada Satisfactoriamente"
    permission_required="inv.add_localidad"



class LocalidadEdit(SuccessMessageMixin,SinPrivilegios, \
    generic.UpdateView):
    permission_required="domicilios.change_localidad"
    model=Provincia
    template_name="localidades/localidad_form.html"
    context_object_name = "obj"
    form_class=LocalidadForm
    success_url=reverse_lazy("dom:localidad_list")
    success_message="Localidad Actualizada Satisfactoriamente"




'''
def eliminar_domicilio(request, id):
    domicilio = Domicilio.objects.get(pk=id)
    domicilio.baja = True
    domicilio.fecha_baja = datetime.datetime.now().date()
    domicilio.save()
    messages.success(request, "El domicilio se eliminó correctamente")
    return redirect(to="/clientes/listado")


class DomicilioUpdateView(UpdateView):

    template_name = 'domicilio_form.html'
    model = Domicilio
    form_class = DomicilioForm
    success_url = '/clientes/listado'
    success_message = 'El domicilio fue actualizado con éxito'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['id_domicilio'] = self.kwargs['pk']
        context['id_provincia'] = self.kwargs['pk']
        context['id_localidad'] = self.kwargs['pk']
        context['id_barrio'] = self.kwargs['pk']

        return context

'''