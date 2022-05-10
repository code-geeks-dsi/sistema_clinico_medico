# Generated by Django 3.2.12 on 2022-05-10 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_expediente', '0009_auto_20220508_0151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contieneconsulta',
            name='estado_cola_medica',
            field=models.CharField(choices=[('1', 'Pendiente'), ('2', 'Parcialmente pagado'), ('3', 'Pagado')], max_length=20),
        ),
        migrations.AlterField(
            model_name='contieneconsulta',
            name='fase_cola_medica',
            field=models.CharField(choices=[('1', 'Agendado'), ('2', 'Anotado'), ('3', 'Preparado'), ('4', 'En espera'), ('5', 'En consulta'), ('6', 'Finalizado')], max_length=20),
        ),
    ]
