# Generated by Django 2.2.13 on 2021-06-24 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='email',
            field=models.EmailField(default=1, max_length=250, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='telefono',
            field=models.PositiveIntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
