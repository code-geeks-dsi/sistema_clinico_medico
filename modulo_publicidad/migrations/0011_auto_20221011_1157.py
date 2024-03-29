# Generated by Django 3.2.12 on 2022-10-11 11:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_publicidad', '0010_descuento_porcentaje_descuento'),
    ]

    operations = [
        migrations.AddField(
            model_name='descuento',
            name='fecha_creacion',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='descuento',
            name='fecha_ultima_edicion',
            field=models.DateField(auto_now=True),
        ),
    ]
