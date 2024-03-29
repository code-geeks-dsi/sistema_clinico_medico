# Generated by Django 3.2.12 on 2022-10-29 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_expediente', '0033_auto_20221029_0336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signosvitales',
            name='unidad_frecuencia_cardiaca',
            field=models.CharField(blank=True, default='PPM', max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='signosvitales',
            name='unidad_presion_arterial_diastolica',
            field=models.CharField(blank=True, default='mmHH', max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='signosvitales',
            name='unidad_presion_arterial_sistolica',
            field=models.CharField(blank=True, default='mmHH', max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='signosvitales',
            name='unidad_saturacion_oxigeno',
            field=models.CharField(blank=True, default='%', max_length=1, null=True),
        ),
    ]
