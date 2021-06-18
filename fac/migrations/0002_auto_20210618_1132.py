# Generated by Django 2.2.13 on 2021-06-18 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domicilios', '0002_delete_domicilio'),
        ('fac', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='altura',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='barrio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='domicilios.Barrio'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cliente',
            name='calle',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='departamento',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='manzana',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='observacion',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='piso',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='tipo',
            field=models.CharField(choices=[('Física', 'Física'), ('Jurídica', 'Jurídica')], default='Física', max_length=10),
        ),
    ]
