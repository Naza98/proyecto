from domicilios.models import Provincia, Localidad, Barrio
from django.shortcuts import render,redirect
from django.views import generic

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages

from django.contrib.auth import authenticate

from bases.views import SinPrivilegios

from .models import Cliente, FacturaEnc, FacturaDet, FormaPago, TipoFactura
from cmp.models import ComprasEnc
from .forms import ClienteForm
import inv.views as inv
from inv.models import Producto, TipoMovimiento, Movimiento
from django.db.models import Sum

class ClienteView(SinPrivilegios, generic.ListView):
    model = Cliente
    template_name = "fac/cliente_list.html"
    queryset = Cliente.objects.filter(estado=True).exclude(nombres="final")
    obj = queryset
    context_object_name = "obj"
    permission_required="fac.view_cliente"


class VistaBaseCreate(SuccessMessageMixin,SinPrivilegios, \
    generic.CreateView):
    context_object_name = 'obj'
    success_message="Registro Agregado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class VistaBaseEdit(SuccessMessageMixin,SinPrivilegios, \
    generic.UpdateView):
    context_object_name = 'obj'
    success_message="Registro Actualizado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class ClienteNew(VistaBaseCreate):
    model=Cliente
    template_name="fac/cliente_form.html"
    form_class=ClienteForm
    success_url= 'reverse_lazy("fac:cliente_list")'
    permission_required="fac.add_cliente"

    def get_context_data(self, **kwargs):
        context = super(ClienteNew, self).get_context_data(**kwargs)
        context["provincias"] = Provincia.objects.all()
        context["localidades"] = Localidad.objects.all()
        context["barrios"] = Barrio.objects.all()
        return context



class ClienteEdit(VistaBaseEdit):
    model=Cliente
    template_name="fac/cliente_form.html"
    form_class=ClienteForm
    success_url= reverse_lazy("fac:cliente_list")
    permission_required="fac.change_cliente"


    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')

        context = super(ClienteEdit, self).get_context_data(**kwargs)
        context["provincias"] = Provincia.objects.all()
        context["localidades"] = Localidad.objects.all()
        context["barrios"] = Barrio.objects.all()
        context["obj"] = Cliente.objects.filter(pk=pk).first()
        return context


@login_required(login_url="/login/")
@permission_required("fac.change_cliente",login_url="/login/")
def clienteInactivar(request,id):
    cliente = Cliente.objects.filter(pk=id).first()
    contexto = {}
    template_name ="fac/cliente_del.html"

    if not cliente:
        return redirect("inv:cliente_list")
    
    if request.method=='GET':
        contexto={'obj':cliente}

    if request.method=="POST":
        if cliente:
            cliente.estado=False
            cliente.save()
            messages.error(request, 'Cliente Inactivado')
            return redirect("fac:cliente_list")
    return render(request,template_name,contexto)     
   

class FacturaView(SinPrivilegios, generic.ListView):
    model = FacturaEnc
    template_name = "fac/factura_list.html"
    context_object_name = "obj"
    permission_required="fac.view_facturaenc"

    def get_queryset(self):
        user = self.request.user
        # print(user,"usuario")
        qs = super().get_queryset()
        for q in qs:
            print(q.uc,q.id)
        
        if not user.is_superuser:
            qs = qs.filter(uc=user)

        for q in qs:
            print(q.uc,q.id)

        return qs


@login_required(login_url='/login/')
@permission_required('fac.change_facturaenc', login_url='bases:sin_privilegios')
def facturas(request,id=None):
    template_name='fac/facturas.html'

    detalle = {}
    clientes = Cliente.objects.filter(estado=True)
    forma_pago = FormaPago.objects.all()
    tipo_factura = TipoFactura.objects.all()
    
    if request.method == "GET":
        enc = FacturaEnc.objects.filter(pk=id).first()
        if id:
            if not enc:
                messages.error(request,'Esta factura no Existe')
                return redirect("fac:factura_list")

            usr = request.user
            if not usr.is_superuser:
                if enc.uc != usr:
                    messages.error(request,'Esta factura no fue creada por el usuario activo')
                    return redirect("fac:factura_list")

        if not enc:
            encabezado = {
                'id':0,
                'fecha':datetime.today(),
                'cliente':0,
                'tipo_factura':0,
                'forma_pago':0,
                'sub_total':0.00,
                'descuento':0.00,
                'total': 0.00
            }
            detalle=None
        else:
            encabezado = {
                'id':enc.id,
                'fecha':enc.fecha,
                'cliente':enc.cliente,
                'tipo_factura':enc.tipo_factura,
                'forma_pago':enc.forma_pago,
                'sub_total':enc.sub_total,
                'descuento':enc.descuento,
                'total':enc.total
            }

        detalle=FacturaDet.objects.filter(factura=enc)
        contexto = {"enc":encabezado,"det":detalle,"clientes":clientes,"tipo_factura":tipo_factura, "forma_pago":forma_pago}
        return render(request,template_name,contexto)
    
    if request.method == "POST":
        forma_pago = request.POST.get("forma_pago")
        tipo_factura = request.POST.get("tipo_factura")
        cliente = request.POST.get("enc_cliente")
        fecha  = request.POST.get("fecha")
        cli=Cliente.objects.get(pk=cliente)
        fp = FormaPago.objects.get(pk=forma_pago)
        tf = TipoFactura.objects.get(pk=tipo_factura)

        if not id:
            enc = FacturaEnc(
                cliente = cli,
                fecha = fecha,
                forma_pago = fp,
                tipo_factura = tf
            )
            if enc:
                enc.save()
                id = enc.id
        else:
            enc = FacturaEnc.objects.filter(pk=id).first()
            if enc:
                enc.cliente = cli
                enc.save()

        if not id:
            messages.error(request,'No es posible continuar, no se detectó el No. de Factura')
            return redirect("fac:factura_list")
        
        codigo = request.POST.get("codigo")
        cantidad = request.POST.get("cantidad")
        precio = request.POST.get("precio")
        s_total = request.POST.get("sub_total_detalle")
        descuento = request.POST.get("descuento_detalle")
        total = request.POST.get("total_detalle")

        prod = Producto.objects.get(codigo=codigo)
        det = FacturaDet(
            factura = enc,
            producto = prod,
            cantidad = cantidad,
            precio = precio,
            sub_total = s_total,
            descuento = descuento,
            total = total
        )
        
        if det:
            det.save()
            messages.success(request, "Registro agregado correctamente")
        
        return redirect("fac:factura_edit",id=id)

    return render(request,template_name,contexto)


class ProductoView(inv.ProductoView):
    template_name="fac/buscar_producto.html" 


def borrar_detalle_factura(request, id):
    template_name = "fac/factura_borrar_detalle.html"

    det = FacturaDet.objects.get(pk=id)

    if request.method=="GET":
        context={"det":det}

    if request.method == "POST":
        usr = request.POST.get("usuario")
        pas = request.POST.get("pass")

        user =authenticate(username=usr,password=pas)

        if not user:
            return HttpResponse("Usuario o Clave Incorrecta")
        
        if not user.is_active:
            return HttpResponse("Usuario Inactivo")

        if user.is_superuser or user.has_perm("fac.sup_caja_facturadet"):
            det.delete()
            messages.error(request, "Detalle Eliminado Correctamente")
            return HttpResponse("ok")

        return HttpResponse("Usuario no autorizado")
    
    return render(request,template_name,context)


#------------------------Devoluciones--------------------------------------#


#-----------------------Informes estadisticos-------------------------------#

def GraficoVentas(request):

    ventas = FacturaEnc.objects.filter(fecha__year=datetime.now().year).order_by('fecha')
    template_name = 'fac/informes_estadisticos/venta_report_line.html'
    context = {"ventas":ventas}

    return render(request, template_name, context)




def CmpFac(request):

    compras = ComprasEnc.objects.annotate(total_compras=Sum('total'))     
    ventas = FacturaEnc.objects.annotate(total_ventas=Sum('total'))     
    template_name = 'fac/informes_estadisticos/totales.html'
    context = {
        "ventas":ventas,
        "compras":compras
    }
    return render(request, template_name, context)
