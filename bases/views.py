from cmp.models import ComprasEnc
from inv.models import Categoria, Producto, SubCategoria
from django.db.models.aggregates import Sum
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin,\
     PermissionRequiredMixin
from django.views import generic
from datetime import datetime
from fac.models import FacturaEnc, FacturaDet
from inv.models import Producto
from django.db.models import Count



class MixinFormInvalid:
    def form_invalid(self,form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

class SinPrivilegios(LoginRequiredMixin, PermissionRequiredMixin, MixinFormInvalid):
    login_url = 'bases:login'
    raise_exception=False                  #Que no se levante el error 403
    redirect_field_name="redirecto_to"    

    def handle_no_permission(self):         #Es para cuando el usuario quiere acceder a una vista y no tiene permisos
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user==AnonymousUser():
            self.login_url='bases:sin_privilegios'      #Lo va a llevar al archivo de html de los usuarios sin provilegios
        return HttpResponseRedirect(reverse_lazy(self.login_url))


#Inicio del sistema
class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = 'bases/home.html'
    login_url='bases:login' #Si el usuario no esta registrado, enviar al login

    def get_totales_ventas(self):
        data = []
        ventas = FacturaEnc.objects.all().aggregate(ventas=Sum('total'))
        data.append(ventas)
        return ventas["ventas"]
    
    def get_totales_compras(self):
        data = []
        compras = ComprasEnc.objects.all().aggregate(compras=Sum('total'))
        data.append(compras)
        return compras["compras"]

    def ProductosMasVendidos(self):
        data = []
        produ = FacturaDet.objects.all() \
        .filter(factura_id__in=FacturaEnc) \
        .values('producto__nombre_producto') \
        .annotate(total=Sum('cantidad')).order_by('total')[:5]
        data.append(produ)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['totales_ventas'] = self.get_totales_ventas()
        context['totales_compras'] = self.get_totales_compras()
        context['produ_mas_vendidos'] = self.ProductosMasVendidos
        return context



class HomeSinPrivilegios(LoginRequiredMixin, generic.TemplateView):
    login_url = "bases:login"
    template_name="bases/sin_privilegios.html"






#---------------------------------------------------------------------#

def total_ventas(request):

    ventas = FacturaDet.objects.all().filter(facturaenc_id__in=FacturaEnc) \
        .values('producto__nombre_producto', 'cantidad') \
        .annotate(total=Sum('cantidad')).order_by('total')
        
    contexto = {'ventas':ventas}
    template_name = 'bases/home.html'
    return render(request,template_name,contexto)  



# Los 5 productos mas vendidos 
def CantidadProductosVendidos(request):
    qs = Producto.objects.annotate(num_prod=Sum('facturadet__cantidad')).order_by('-num_prod')[:5]
    import json
    data ={}                                                            
    c = 0                                                              
    for p in qs:                                                      
        obj = {                                                        
            c: {                                                       
                "label":p.nombre_producto,
                "cantidad":p.num_prod
            } 
        }
        data.update(obj)                                                
        c = c + 1 
    return JsonResponse(data)

# Los 5 Productos menos vendidos
def ProductosMenosVendidos(request):
    qs = Producto.objects.annotate(num_prod=Sum('facturadet__cantidad')).order_by('num_prod')[:5]
    import json
    data ={}                                                            
    c = 0                                                            
    for p in qs:                                                       
        obj = {                                                        
            c: {                                                        
                "productos":p.nombre_producto,
                "numeros":p.num_prod
            } 
        }
        data.update(obj)                                                
        c = c + 1 
    return JsonResponse(data)

# Productos mas vendidos por 
def ProductosPorCategoria(request):
    qs = Producto.objects.values('subcategoria').annotate(num_prod=Sum('facturadet__cantidad')).order_by('-num_prod')
    import json
    data ={}                                                            
    c = 0                                                            
    for p in qs:                                                       
        obj = {                                                        
            c: {                                                        
                "label":p.subcategoria,
                "data":p.num_prod
            } 
        }
        data.update(obj)                                                
        c = c + 1 
    return JsonResponse(data)


#cantidad = Producto.objects.values('subcategoria').annotate(num_prod=Sum('facturadet__cantidad')).order_by('-num_prod')
#print(cantidad)


