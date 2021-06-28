# Generated by Django 2.2.13 on 2021-06-24 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialPreciosVenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_modificacion', models.DateField(auto_created=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=12)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inv.Producto')),
            ],
            options={
                'verbose_name': 'Historial de Precios de Venta',
                'verbose_name_plural': 'Historiales de Precios de Ventas',
            },
        ),
    ]