# Generated by Django 2.2.13 on 2021-06-26 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0003_auto_20210626_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='foto',
            field=models.ImageField(blank=True, default='images/no_imagen.png', null=True, upload_to='images/'),
        ),
    ]