from django.db import models

from bases.models import ClaseModelo
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


'''

Aplicacion de inventario

'''

class Categoria(ClaseModelo):
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripción de la Categoría',
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper() #Colocar todas las letras en mayuscula
        super(Categoria, self).save() #Guardar

    class Meta:
        verbose_name_plural= "Categorias"


class SubCategoria(ClaseModelo):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripción de la Categoría'
    )

    def __str__(self):
        return '{}:{}'.format(self.categoria.descripcion,self.descripcion)
    
    def save(self):
        self.descripcion = self.descripcion.upper()
        super(SubCategoria, self).save()

    class Meta:
        verbose_name_plural= "Sub Categorias"
        unique_together = ('categoria','descripcion')


class Marca(ClaseModelo):
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripción de la Marca',
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Marca, self).save()

    class Meta:
        verbose_name_plural = "Marca"

'''
class UnidadMedida(ClaseModelo):
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripción de la Unidad Medida',
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(UnidadMedida, self).save()

    class Meta:
        verbose_name_plural = "Unidades de Medida"
'''

class Producto(ClaseModelo):
    codigo = models.CharField(max_length=20,unique=True, auto_created=True)
    nombre_producto = models.CharField(max_length=300)
    codigo_barra = models.CharField(max_length=50, unique=True, auto_created=True)
    descripcion = models.CharField(max_length=300)
    precio = models.FloatField(default=0)
    precio_anterior = models.IntegerField(null=True, blank=True, default=0)
    existencia = models.IntegerField(default=0)
    ultima_compra = models.DateField(null=True, blank=True)

    stock_minimo = models.IntegerField(null=True, blank=True, default=0)


    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    #unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to="images/",null=True,blank=True, default='images/no_imagen.png')

    def __str__(self):
        return '{}'.format(self.nombre_producto)
    
    def save(self):
        self.nombre_producto = self.nombre_producto.upper()
        super(Producto,self).save()
    
    class Meta:
        verbose_name_plural = "Productos"
        unique_together = ('codigo','codigo_barra')



class HistorialPreciosVenta(models.Model):

    ''' guarda el historial de precios
    de ventas, a medida que se va cambiando  '''

    producto = models.ForeignKey(Producto, null=False, blank=False, on_delete=models.CASCADE)
    fecha_modificacion = models.DateField(auto_created=True)
    precio = models.DecimalField(decimal_places=2, max_digits=12,
                                 null=False, blank=False)

    def __str__(self):
        return str(self.precio)

    class Meta:

        verbose_name = 'Historial de Precios de Venta'
        verbose_name_plural = 'Historiales de Precios de Ventas'
        permissions = [
            ('historial_precios_venta','Historial de precios de venta')
        ]

#--------------------PARA LOS AJUSTES DE INVENTARIO Y DEVOLUCIONES--------------------------#

class TipoMovimiento(ClaseModelo):
    '''
    compra, venta, ajuste_incremento, ajuste_disminucion, rotura, perdida, actualizacion de precios
    '''
    descripcion = models.CharField(max_length=300, null=False, blank=False)

    class Meta:
        verbose_name = 'Tipo de movimiento'
        verbose_name_plural = 'Tipo de movimientos'
        db_table = 'Tipo de movimientos'


class Motivo(ClaseModelo):

    descripcion = models.CharField(max_length=300, null=False, blank=False)

    class Meta:
        verbose_name = 'Motivo'
        verbose_name_plural = 'Motivos'
        db_table = 'Motivos'


class Movimiento(ClaseModelo):

    producto = models.ForeignKey(Producto, null=False, blank=False, on_delete=models.CASCADE)
    tipo_movimiento = models.ForeignKey(TipoMovimiento, null=False, blank=False, on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True)
    cantidad = models.IntegerField(null=True, blank=True)
    #En caso de que sea una devolucion, se debe especificar el motivo.
    motivo = models.ForeignKey(Motivo, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Movimientos'
        verbose_name_plural = 'Movimientos'
        db_table = 'Movimientos'



@receiver(post_save, sender=Movimiento)
def aumento(sender,instance,**kwargs):
    id_producto = instance.producto.id
    id_tipo_movimiento = instance.tipo_movimiento.id
    fecha=instance.fecha
    cantidad=instance.cantidad

    prod=Producto.objects.filter(pk=id_producto).first()
    if id_tipo_movimiento == 1:
        if prod:
            cantidad = int(prod.existencia) + int(instance.cantidad)
            prod.existencia = cantidad
            prod.save()            


@receiver(post_save, sender=Movimiento)
def disminucion(sender,instance,**kwargs):
    id_producto = instance.producto.id
    id_tipo_movimiento = instance.tipo_movimiento.id
    fecha=instance.fecha
    cantidad=instance.cantidad

    prod=Producto.objects.filter(pk=id_producto).first()
    if id_tipo_movimiento == 2:
        if prod:
            cantidad = int(prod.existencia) - int(instance.cantidad)
            prod.existencia = cantidad
            prod.save()           

#---------------------------------FIN AJUSTE INVENTARIO----------------------------#

