from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from inv.models import Producto
from fac.models import Cliente
class Presupuesto(models.Model):

    productom=Producto()
    
    producto=models.ForeignKey(Producto, on_delete=models.DO_NOTHING) #con esto traigo los productos disponibles.
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    precio_unitario=models.FloatField(default=1)
    cantidad=models.IntegerField(default=1)
    total=models.FloatField()
    plazo = models.DateField(null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)
    
    
    class Meta:
        verbose_name_plural = "Presupuestos"
        verbose_name="Presupuestos"