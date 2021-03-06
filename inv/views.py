from django.db.models import query
from django.db.models.aggregates import Sum
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import datetime

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required


from .models import Categoria,SubCategoria, Marca, \
    Producto, TipoMovimiento, Motivo, Movimiento, HistorialPreciosVenta
from .forms import ActualizacionPrecioForm, CategoriaForm, SubCategoriaForm, MarcaForm, \
    ProductoForm, MovimientoForm

from bases.views import SinPrivilegios


class CategoriaView(SinPrivilegios, generic.ListView):
    permission_required = "inv.view_categoria" #permiso para acceder al la lista 
    model = Categoria
    queryset = Categoria.objects.filter(estado=True).order_by('descripcion')
    obj = queryset
    template_name = "inv/categoria_list.html"
    context_object_name = "obj"
    


class CategoriaNew(SuccessMessageMixin,SinPrivilegios,\
    generic.CreateView):
    permission_required="inv.add_categoria"
    model=Categoria
    template_name="inv/categoria_form.html"
    context_object_name = "obj"
    form_class=CategoriaForm
    success_url=reverse_lazy("inv:categoria_list")
    success_message="Categoria Creada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class CategoriaEdit(SuccessMessageMixin,SinPrivilegios, \
    generic.UpdateView):
    permission_required="inv.change_categoria"
    model=Categoria
    template_name="inv/categoria_form.html"
    context_object_name = "obj"
    form_class=CategoriaForm
    success_url=reverse_lazy("inv:categoria_list")
    success_message="Categoria Actualizada Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)



@login_required(login_url="/login/")
@permission_required("inv.change_categoria",login_url="bases:sin_privilegios")
def categoria_inactivar(request, id):
    prod = Categoria.objects.filter(pk=id).first()
    contexto={}
    template_name="inv/catalogos_del.html"

    if not prod:
        return redirect("inv:categoria_list")
    
    if request.method=='GET':
        contexto={'obj':prod}
    
    if request.method=='POST':
        prod.estado=False
        prod.save()
        messages.error(request, 'Categor??a Inactivada Satisfactoriamente')
        return redirect("inv:categoria_list")

    return render(request,template_name,contexto)

'''
class CategoriaDel(SuccessMessageMixin,SinPrivilegios, generic.DeleteView):
    permission_required="inv.delete_categoria"
    model=Categoria
    template_name='inv/catalogos_del.html'
    context_object_name='obj'
    success_url=reverse_lazy("inv:categoria_list")
    success_message="Categor??a Eliminada Satisfactoriamente"
'''


class SubCategoriaView(SinPrivilegios, \
    generic.ListView):
    permission_required = "inv.view_subcategoria"
    model = SubCategoria
    queryset = SubCategoria.objects.filter(estado=True).order_by('descripcion')
    obj = queryset
    template_name = "inv/subcategoria_list.html"
    context_object_name = "obj"


class SubCategoriaNew(SuccessMessageMixin,SinPrivilegios, generic.CreateView):
    model=SubCategoria
    template_name="inv/subcategoria_form.html"
    context_object_name = "obj"
    form_class=SubCategoriaForm
    success_url=reverse_lazy("inv:subcategoria_list")
    success_message="Sub-Categor??a Creada Satisfactoriamente"
    permission_required="inv.add_subcategoria"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class SubCategoriaEdit(SuccessMessageMixin,SinPrivilegios, generic.UpdateView):
    model=SubCategoria
    template_name="inv/subcategoria_form.html"
    context_object_name = "obj"
    form_class=SubCategoriaForm
    success_url=reverse_lazy("inv:subcategoria_list")
    success_message="Sub-Categor??a Actualizada Satisfactoriamente"
    permission_required="inv.change_subcategoria"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


@login_required(login_url="/login/")
@permission_required("inv.change_subcategoria",login_url="bases:sin_privilegios")
def subcategoria_inactivar(request, id):
    prod = SubCategoria.objects.filter(pk=id).first()
    contexto={}
    template_name="inv/catalogos_del.html"

    if not prod:
        return redirect("inv:subcategoria_list")
    
    if request.method=='GET':
        contexto={'obj':prod}
    
    if request.method=='POST':
        prod.estado=False
        prod.save()
        messages.error(request, 'Sub Categor??a Inactivada Satisfactoriamente')
        return redirect("inv:subcategoria_list")

    return render(request,template_name,contexto)

'''
class SubCategoriaDel(SuccessMessageMixin,SinPrivilegios, generic.DeleteView):
    model=SubCategoria
    template_name='inv/catalogos_del.html'
    context_object_name='obj'
    success_url=reverse_lazy("inv:subcategoria_list")
    success_message="Sub Categor??a Eliminada"
    permission_required="inv.delete_subcategoria"

'''
class MarcaView(SinPrivilegios,\
     generic.ListView):
    permission_required = "inv.view_marca"
    model = Marca
    queryset = Marca.objects.filter(estado=True).order_by('descripcion')
    obj = queryset
    template_name = "inv/marca_list.html"
    context_object_name = "obj"


class MarcaNew(SuccessMessageMixin,SinPrivilegios,
                   generic.CreateView):
    model=Marca
    template_name="inv/marca_form.html"
    context_object_name = 'obj'
    form_class=MarcaForm
    success_url= reverse_lazy("inv:marca_list")
    success_message="Marca Creada Sastifactoriamente"
    permission_required="inv.add_marca"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class MarcaEdit(SuccessMessageMixin,SinPrivilegios,
                   generic.UpdateView):
    model=Marca
    template_name="inv/marca_form.html"
    context_object_name = 'obj'
    form_class=MarcaForm
    success_url= reverse_lazy("inv:marca_list")
    success_message="Marca Editada Satisfactoriamente"
    permission_required="inv.change_marca"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


@login_required(login_url='/login/')
@permission_required('inv.change_marca', login_url='bases:sin_privilegios')
def marca_inactivar(request, id):
    marca = Marca.objects.filter(pk=id).first()
    contexto={}
    template_name="inv/catalogos_del.html"

    if not marca:
        return redirect("inv:marca_list")
    
    if request.method=='GET':
        contexto={'obj':marca}
    
    if request.method=='POST':
        marca.estado=False
        marca.save()
        messages.error(request, 'Marca Inactivada')
        return redirect("inv:marca_list")

    return render(request,template_name,contexto)

'''
class UMView(SinPrivilegios, generic.ListView):
    model = UnidadMedida
    template_name = "inv/um_list.html"
    context_object_name = "obj"
    permission_required="inv.view_unidadmedida"


class UMNew(SuccessMessageMixin,SinPrivilegios,
                   generic.CreateView):
    model=UnidadMedida
    template_name="inv/um_form.html"
    context_object_name = 'obj'
    form_class=UMForm
    success_url= reverse_lazy("inv:um_list")
    success_message="Unidad Medida Creada"
    permission_required="inv.add_unidadmedida"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        print(self.request.user.id)
        return super().form_valid(form)


class UMEdit(SuccessMessageMixin,SinPrivilegios,
                   generic.UpdateView):
    model=UnidadMedida
    template_name="inv/um_form.html"
    context_object_name = 'obj'
    form_class=UMForm
    success_url= reverse_lazy("inv:um_list")
    success_message="Unidad Medida Editada"
    permission_required="inv.change_unidadmedida"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        print(self.request.user.id)
        return super().form_valid(form)


@login_required(login_url="/login/")
@permission_required("inv.change_unidadmedida",login_url="/login/")
def um_inactivar(request, id):
    um = UnidadMedida.objects.filter(pk=id).first()
    contexto={}
    template_name="inv/catalogos_del.html"

    if not um:
        return redirect("inv:um_list")
    
    if request.method=='GET':
        contexto={'obj':um}
    
    if request.method=='POST':
        um.estado=False
        um.save()
        return redirect("inv:um_list")

    return render(request,template_name,contexto)
'''

class ProductoView(SinPrivilegios, generic.ListView):
    model = Producto
    template_name = "inv/producto_list.html"
    queryset = Producto.objects.filter(estado=True).order_by('nombre_producto')
    obj = queryset
    context_object_name = "obj"
    permission_required="inv.view_producto"


class ProductoDetail(SinPrivilegios, generic.DetailView):
    model = Producto   
    template_name = "inv/producto_detail.html"
    permission_required="inv.view_producto"




class ProductoNew(SuccessMessageMixin,SinPrivilegios,
                   generic.CreateView):
    model=Producto
    template_name="inv/producto_form.html"
    context_object_name = 'obj'
    form_class=ProductoForm
    success_url= reverse_lazy("inv:producto_list")
    success_message="Producto Creado Satisfactoriamente"
    permission_required="inv.add_producto"

    def form_valid(self, form):                 
        form.instance.uc = self.request.user #instancia el usuario que esta logueado, el que crea el registro
        return super().form_valid(form)      #retorna la validacion 
    
    def get_context_data(self, **kwargs):
        context = super(ProductoNew, self).get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.all()
        context["subcategorias"] = SubCategoria.objects.all()
        return context



class ProductoEdit(SuccessMessageMixin,SinPrivilegios,
                   generic.UpdateView):
    model=Producto
    template_name="inv/producto_form.html"
    context_object_name = 'obj'
    form_class=ProductoForm
    success_url= reverse_lazy("inv:producto_list")
    success_message="Producto Editado Satisfactoriamente"
    permission_required="inv.change_producto"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        form.instance.fm = datetime.now().date()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')

        context = super(ProductoEdit, self).get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.all()
        context["subcategorias"] = SubCategoria.objects.all()
        context["obj"] = Producto.objects.filter(pk=pk).first()
        return context


@login_required(login_url="/login/")
@permission_required("inv.change_producto",login_url="bases:sin_privilegios")
def producto_inactivar(request, id):
    prod = Producto.objects.filter(pk=id).first()
    contexto={}
    template_name="inv/producto_del.html"

    if not prod:
        return redirect("inv:producto_list")
    
    if request.method=='GET':
        contexto={'obj':prod}
    
    if request.method=='POST':
        prod.estado=False
        prod.save()
        messages.error(request, 'Producto Inactivado')
        return redirect("inv:producto_list")

    return render(request,template_name,contexto)


class HistorialPreciosProductos(SinPrivilegios,\
     generic.ListView):

    model = HistorialPreciosVenta
    template_name = 'inv/historial_precios.html'
    queryset = HistorialPreciosVenta.objects.all().order_by('fecha_modificacion', 'producto__nombre_producto')
    obj = queryset
    context_object_name = "obj"
    permission_required="inv.historial_precios_venta"

    def get_context_data(self, **kwargs):
        context = super(HistorialPreciosProductos, self).get_context_data(**kwargs)
        context["productos"] = Producto.objects.all()
        return context


class MovimientoView(SinPrivilegios, generic.ListView):
    model = Movimiento
    template_name = "movimientos/movimiento_list.html"
    queryset = Movimiento.objects.all()
    obj = queryset
    context_object_name = "obj"
    permission_required="inv.view_movimiento"


class MovimientoNew(SuccessMessageMixin,SinPrivilegios,
                   generic.CreateView):
    model=Movimiento
    template_name="movimientos/movimiento_form.html"
    context_object_name = 'obj'
    form_class=MovimientoForm
    success_url= reverse_lazy("inv:movimiento_list")
    success_message="Ajuste Realizado Satisfactoriamente"
    permission_required="inv.add_movimiento"

    def form_valid(self, form):                 
        form.instance.uc = self.request.user #instancia el usuario que esta logueado, el que crea el registro
        return super().form_valid(form)      #retorna la validacion 
    
    def get_context_data(self, **kwargs):
        context = super(MovimientoNew, self).get_context_data(**kwargs)
        context["productos"] = Producto.objects.filter(estado=True).order_by('nombre_producto')
        context["tipo_movimiento"] = TipoMovimiento.objects.all()
        context["motivos"] = Motivo.objects.all()
        return context



class MovimientoEdit(SuccessMessageMixin,SinPrivilegios,
                   generic.UpdateView):
    model=Movimiento
    template_name="movimientos/movimiento_form.html"
    context_object_name = 'obj'
    form_class=MovimientoForm
    success_url= reverse_lazy("inv:movimiento_list")
    success_message="Movimiento Editado Satisfactoriamente"
    permission_required="inv.change_movimiento"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        form.instance.fm = datetime.now().date()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')

        context = super(MovimientoEdit, self).get_context_data(**kwargs)
        context["productos"] = Producto.objects.all()
        context["tipo_movimiento"] = TipoMovimiento.objects.all()
        context["motivos"] = Motivo.objects.all()
        context["obj"] = Movimiento.objects.filter(pk=pk).first()
        return context



#-----------------------Actualizar precios----------------------------------#

class ActualizarPrecioTemplateView(generic.TemplateView):

    template_name = 'inv/producto_actualizar_precios.html'

    def get_context_data(self, **kwargs):
        context = super(ActualizarPrecioTemplateView, self)\
            .get_context_data(**kwargs)
        context['form'] = ActualizacionPrecioForm()
        return context

    def post(self, request, *args,  **kwargs):
        busqueda = {}
        form_producto_actualizar = ActualizacionPrecioForm(data=
                                                           self.request.POST)
        if form_producto_actualizar.is_valid():

            if 'subcategoria' in form_producto_actualizar.data:
                if form_producto_actualizar.data['subcategoria'] != '':
                    busqueda['subcategoria__id'] = form_producto_actualizar.data['subcategoria']
            productos = Producto.objects.filter(**busqueda)        
            if 'variacion' in form_producto_actualizar.data:
                if form_producto_actualizar.data['variacion'] == 'venta':
                    if 'moneda' in form_producto_actualizar.data:
                        if form_producto_actualizar.data['moneda'] == 'pesos':

                            for producto in productos:
                                resultado = str(int(producto.precio) + \
                                                int(form_producto_actualizar.data[
                                                        'numero']))

                                historial_precio_venta = HistorialPreciosVenta(
                                    producto=producto,
                                    fecha_modificacion=datetime.now(),
                                    precio=producto.precio)
                                historial_precio_venta.save()

                                producto.precio = resultado
                                producto.save()
                        else:
                            for producto in productos:
                                aumento = (int(producto.precio) *
                                           int(form_producto_actualizar.
                                               data['numero'])) / 100
                                resultado = int(producto.precio) + \
                                            int(aumento)

                                historial_precio_venta = HistorialPreciosVenta(
                                    producto=producto,
                                    fecha_modificacion=datetime.now(),
                                    precio=producto.precio)
                                historial_precio_venta.save()

                                producto.precio = resultado
                                producto.save()

            messages.success(self.request, 'Los precios de los productos se modificaron correctamente')
            return HttpResponseRedirect('/inv/productos/')
        else:
            return render(self.request,
                          'inv/producto_actualizar_precios.html',
                          {'form': form_producto_actualizar})


def ProductosMenosVendidos(request):
    qs = Producto.objects.annotate(num_prod=Sum('facturadet__cantidad')).order_by('num_prod')[:5]
    import json
    data ={}                                                            
    c = 0                                                            
    for p in qs:                                                       
        obj = {                                                        
            c: {                                                        
                "label":p.nombre_producto,
                "data":p.num_prod
            } 
        }
        data.update(obj)                                                
        c = c + 1 
    return JsonResponse(data)