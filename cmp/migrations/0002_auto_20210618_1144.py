# Generated by Django 2.2.13 on 2021-06-18 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domicilios', '0002_delete_domicilio'),
        ('cmp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proveedor',
            name='direccion',
        ),
        migrations.AddField(
            model_name='proveedor',
            name='altura',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='barrio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='domicilios.Barrio'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proveedor',
            name='calle',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='departamento',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='manzana',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='observacion',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='piso',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='email',
            field=models.EmailField(blank=True, max_length=250, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='telefono',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
