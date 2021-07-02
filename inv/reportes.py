import os
import cgi
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils import timezone
from .models import HistorialPreciosVenta, Producto, Movimiento

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path



def historial_precios_productos(request):
    template_path = 'inv/historial_precios_print_all.html' #ruta a nuestra plantilla
    today = timezone.now() #fecha actual 

    historial = HistorialPreciosVenta.objects.order_by('fecha_modificacion', 'producto__nombre_producto')
    productos = Producto.objects.filter(estado=True).order_by('nombre_producto')
    context = {
        'obj': historial,  #todas las actulizaciones
        'today': today,  #fecha actual
        'request': request, #respuesta
        'productos':productos
        }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf') #objeto de respuesta 
    response['Content-Disposition'] = 'inline; filename="report.pdf"' #asignar la forma en la que se va a mostrar  
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context) #renderizamos el contexto

    # create a pdf
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def imprimir_movimientos(request):
    template_path = 'movimientos/movimientos_print_all.html' #ruta a nuestra plantilla
    today = timezone.now() #fecha actual 

    movimientos = Movimiento.objects.order_by('fecha', 'producto__nombre_producto')
    context = {
        'obj': movimientos,  #todas las actulizaciones
        'today': today,  #fecha actual
        'request': request, #respuesta
        }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf') #objeto de respuesta 
    response['Content-Disposition'] = 'inline; filename="report.pdf"' #asignar la forma en la que se va a mostrar  
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context) #renderizamos el contexto

    # create a pdf
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def movimiento_unico(request, movimiento_id):
    template_path = 'movimientos/movimiento_print_one.html'
    today = timezone.now()
    
    movimiento = Movimiento.objects.filter(id=movimiento_id).first()
    if movimiento:
        detalle = Movimiento.objects.filter(id=movimiento_id)
    else:
        detalle={}
    
    context = {
        'movimiento':movimiento,
        'detalle':detalle,
        'today':today,
        'request': request
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response