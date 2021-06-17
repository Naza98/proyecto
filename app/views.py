from django.shortcuts import render,redirect
from django.views import generic

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages
from django.db.models import Sum

from bases.views import SinPrivilegios

from fac.models import Cliente, FacturaEnc, FacturaDet
from inv.models import Producto

def total_ventas(request):

    ventas = FacturaDet.objects.all().filter(facturaenc_id__in=FacturaEnc) \
        .values('producto__nombre_producto', 'cantidad') \
        .annotate(total=Sum('cantidad')).order_by('total')
        
    contexto = {'ventas':ventas}
    template_name = 'bases/home.html'
    return render(request,template_name,contexto)  