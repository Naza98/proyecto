from django import template
from django.contrib import messages
from django.shortcuts import render

# Create your views here.
from presupuestos.models import Presupuesto
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse
from presupuestos.forms import PresupuestosForm
import json as simplejson
from inv.models import Producto
from fac.models import Cliente



#ver y guardar presupuestos
def presupuestos_view(request):
 
    if request.method =='POST':
        form=PresupuestosForm(request.POST)
        if form.is_valid():
           form.save()
           messages.success(request,'El presupuesto fue generado con éxito')
           return redirect('pre:presupuestos_view')
    else:
        presupuesto=Presupuesto.objects.all()   
        clientes = Cliente.objects.filter(estado=True).order_by('apellidos')  
        form=PresupuestosForm()   
        return render(request,'presupuestos/presupuestos_list.html', 
                  {'form':form,'losp':presupuesto, 'cliente':clientes})
                  #{'form':form, 'variable':123465}) #para pasar variable al template.



#traer precio cuando se selecciona el producto en el select
def getPrecio(request):
    if request.method == 'GET' and request.is_ajax():
        prod_buscado = request.GET.get('prod', None)
        answer = str(prod_buscado)
        print(prod_buscado)

        selected_prod = Producto.objects.get(nombre_producto=answer)
        precio = selected_prod.precio
        return HttpResponse(simplejson.dumps(precio), content_type='application/json')

    else:
        return redirect('/')


def eliminar(request, id):
    pres = Presupuesto.objects.filter(pk=id).first()
    contexto = {}
    template_name = "presupuestos/presupuesto_del.html"

    if not pres:
        return redirect("pre:presupuestos_view")

    if request.method=="GET":
        contexto = {'obj':pres}

    if request.method=="POST":    
        if pres:
            pres.delete()
            messages.error(request, "El presupuesto fue eliminado correctamente")
            return redirect("pre:presupuestos_view")
    return render(request, template_name, contexto)



#cantidad = Presupuesto.objects.all().count()
#print(cantidad)
