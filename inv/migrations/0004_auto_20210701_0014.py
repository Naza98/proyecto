# Generated by Django 2.2.13 on 2021-07-01 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0003_auto_20210630_2303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historialpreciosventa',
            options={'permissions': [('historial_precios_venta', 'Historial de precios de venta')], 'verbose_name': 'Historial de Precios de Venta', 'verbose_name_plural': 'Historiales de Precios de Ventas'},
        ),
    ]
