# Generated by Django 2.2.13 on 2021-07-02 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='casa',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
