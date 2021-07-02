from django.db import models

#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


'''---------------------- Domicilios ---------------------- '''

class Provincia(models.Model):

    nombre_provincia = models.CharField(max_length=300, null=False, blank=False)

    def __str__(self):
        return self.nombre_provincia

    class Meta:

        db_table = 'Provincias'
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        



class Localidad(models.Model):

    nombre_localidad = models.CharField(max_length=300, null=False, blank=False)
    provincia = models.ForeignKey(Provincia, null=False, blank=False, on_delete=models.CASCADE)


    def __str__(self):
        return self.nombre_localidad

    class Meta:

        db_table = 'Localidades'
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'



class Barrio(models.Model):

    localidad = models.ForeignKey(Localidad, null=False, blank=False,
    on_delete=models.CASCADE)
    nombre_barrio = models.CharField(max_length=300, null=False, blank=False)

    def __str__(self):
        return self.nombre_barrio

    class Meta:

        db_table = 'Barrios'
        verbose_name = 'Barrio'
        verbose_name_plural = 'Barrios'
