from django.shortcuts import render,redirect
from django.views import generic
from django.urls import reverse_lazy
import datetime
from django.http import HttpResponse, JsonResponse


from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
import json
from django.db.models import Sum

from .models import Proveedor, ComprasEnc, ComprasDet
from cmp.forms import ProveedorForm,ComprasEncForm
from bases.views import SinPrivilegios
from inv.models import Producto
from domicilios.models import Provincia, Localidad, Barrio
from fac.models import TipoFactura, FormaPago


class ProveedorView(SinPrivilegios, generic.ListView):
    model = Proveedor
    template_name = "cmp/proveedor_list.html"
    queryset = Proveedor.objects.filter(estado=True).order_by('descripcion')
    obj = queryset
    context_object_name = "obj"
    permission_required="cmp.view_proveedor"

class ProveedorDetail(SinPrivilegios, generic.DetailView):
    model = Proveedor   
    template_name = "cmp/proveedor_detail.html"
    permission_required="cmp.view_proveedor"


class ProveedorNew(SuccessMessageMixin, SinPrivilegios,\
                   generic.CreateView):
    model=Proveedor
    template_name="cmp/proveedor_form.html"
    context_object_name = 'obj'
    form_class=ProveedorForm
    success_url= reverse_lazy("cmp:proveedor_list")
    success_message="Registro Agregado Correctamente"
    permission_required="cmp.add_proveedor"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        #print(self.request.user.id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProveedorNew, self).get_context_data(**kwargs)
        context["provincias"] = Provincia.objects.all()
        context["localidades"] = Localidad.objects.all()
        context["barrios"] = Barrio.objects.all()
        return context


class ProveedorEdit(SuccessMessageMixin, SinPrivilegios,\
                   generic.UpdateView):
    model=Proveedor
    template_name="cmp/proveedor_form.html"
    context_object_name = 'obj'
    form_class=ProveedorForm
    success_url= reverse_lazy("cmp:proveedor_list")
    success_message="Proveedor Editado"
    permission_required="cmp.change_proveedor"
    
    def form_valid(self, form):                        
        form.instance.um = self.request.user.id    #'''Lineas de validaciones'''
        print(self.request.user.id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')

        context = super(ProveedorEdit, self).get_context_data(**kwargs)
        context["provincias"] = Provincia.objects.all()
        context["localidades"] = Localidad.objects.all()
        context["barrios"] = Barrio.objects.all()
        context["obj"] = Proveedor.objects.filter(pk=pk).first()
        return context    


@login_required(login_url="/login/")
@permission_required("cmp.change_proveedor",login_url="/login/")
def proveedorInactivar(request,id):
    template_name='cmp/inactivar_prv.html'
    contexto={}
    prv = Proveedor.objects.filter(pk=id).first()

    if not prv:
        return HttpResponse('Proveedor no existe ' + str(id))

    if request.method=='GET':
        contexto={'obj':prv}

    if request.method=='POST':
        prv.estado=False
        prv.save()
        contexto={'obj':'OK'}
        return HttpResponse('Proveedor Inactivado')

    return render(request,template_name,contexto)


class ComprasView(SinPrivilegios, generic.ListView):
    model = ComprasEnc
    template_name = "cmp/compras_list.html"
    context_object_name = "obj"
    permission_required="cmp.view_comprasenc"


@login_required(login_url='/login/')
@permission_required('cmp.view_comprasenc', login_url='bases:sin_privilegios')
def compras(request,compra_id=None):
    template_name="cmp/compras.html"
    prod=Producto.objects.filter(estado=True).order_by('nombre_producto') #filtar los productos activos 
    #forma_pago = FormaPago.objects.all()
    #tipo_factura = TipoFactura.objects.all()
    form_compras={} #fumulario vacio
    contexto={}

    if request.method=='GET':
        form_compras=ComprasEncForm() #incializar formulario de compras
        enc = ComprasEnc.objects.filter(pk=compra_id).first() #filtar la informacion a mostrar del modelo ComprasEnc

        if enc:     #si existe
            det = ComprasDet.objects.filter(compra=enc) #acceder al modelo detalle 
            fecha_compra = datetime.date.isoformat(enc.fecha_compra) 
            fecha_factura = datetime.date.isoformat(enc.fecha_factura)
            e = {
                'fecha_compra':fecha_compra,
                'proveedor': enc.proveedor,
                'observacion': enc.observacion,
                'no_factura': enc.no_factura,
                'fecha_factura': fecha_factura,
                'sub_total': enc.sub_total,
                'descuento': enc.descuento,
                'total':enc.total
                #'forma_pago': enc.forma_pago,
                #'tipo_factura':enc.tipo_factura
            }
            form_compras = ComprasEncForm(e) #se le pasan los datos al formulario
        else: #si no existe el encabezado
            det=None #detalle sea vacio
        
        contexto={'productos':prod,'encabezado':enc,'detalle':det,'form_enc':form_compras} #se envian los contextos a la plantilla  

    if request.method=='POST':
        #fp = FormaPago.objects.get(pk=forma_pago)
        #tf = TipoFactura.objects.get(pk=tipo_factura)
        fecha_compra = request.POST.get("fecha_compra")
        observacion = request.POST.get("observacion")
        no_factura = request.POST.get("no_factura")
        fecha_factura = request.POST.get("fecha_factura")
        proveedor = request.POST.get("proveedor")
        sub_total = 0
        descuento = 0
        total = 0

        if not compra_id:
            prov=Proveedor.objects.get(pk=proveedor)

            enc = ComprasEnc(
                #forma_pago = fp,
                #tipo_factura = tf,
                fecha_compra=fecha_compra,
                observacion=observacion,
                no_factura=no_factura,
                fecha_factura=fecha_factura,
                proveedor=prov,
                uc = request.user 
            )
            if enc:
                enc.save()
                compra_id=enc.id
        else:
            enc=ComprasEnc.objects.filter(pk=compra_id).first()
            if enc:
                enc.fecha_compra = fecha_compra
                enc.observacion = observacion
                enc.no_factura=no_factura
                enc.fecha_factura=fecha_factura
                enc.um=request.user.id
                enc.save()

        if not compra_id: #si la compra no tiene nada
            return redirect("cmp:compras_list") #refireccionar a lista de compras 
        
        producto = request.POST.get("id_id_producto")
        cantidad = request.POST.get("id_cantidad_detalle")
        precio = request.POST.get("id_precio_detalle")
        sub_total_detalle = request.POST.get("id_sub_total_detalle")
        descuento_detalle  = request.POST.get("id_descuento_detalle")
        total_detalle  = request.POST.get("id_total_detalle")

        prod = Producto.objects.get(pk=producto)

        det = ComprasDet(
            compra=enc,
            producto=prod,
            cantidad=cantidad,
            precio_prv=precio,
            descuento=descuento_detalle,
            costo=0,
            uc = request.user
        )

        if det: #si se logro crear ese objecto, se lo guarda
            det.save()

            sub_total=ComprasDet.objects.filter(compra=compra_id).aggregate(Sum('sub_total')) #sumar todos los detalles que coinciden con esta compra
            descuento=ComprasDet.objects.filter(compra=compra_id).aggregate(Sum('descuento'))
            enc.sub_total = sub_total["sub_total__sum"]
            enc.descuento = descuento["descuento__sum"]
            enc.save()
            messages.success(request, "Registro agregado correctamente")


        return redirect("cmp:compras_edit",compra_id=compra_id)


    return render(request, template_name, contexto)
    

class CompraDetDelete(SinPrivilegios, generic.DeleteView):
    permission_required = "cmp.delete_comprasdet"
    model = ComprasDet
    template_name = "cmp/compras_det_del.html"
    context_object_name = 'obj'
    
    def get_success_url(self):
        compra_id=self.kwargs['compra_id']
        return reverse_lazy('cmp:compras_edit', kwargs={'compra_id': compra_id})


def eliminar_detalle(request,id):
    detalle = ComprasDet.objects.filter(pk=id)
    detalle.delete()
    messages.error(request, "Detalle Eliminado Correctamente")
    return HttpResponse("ok")