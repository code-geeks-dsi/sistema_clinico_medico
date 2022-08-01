# Generated by Django 3.2.12 on 2022-05-28 22:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_control', '0008_auto_20220514_2319'),
        ('modulo_laboratorio', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resultado',
            name='fecha_resultado',
        ),
        migrations.RemoveField(
            model_name='resultado',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='resultado',
            name='parametro',
        ),
        migrations.AddField(
            model_name='esperaexamen',
            name='fecha',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='esperaexamen',
            name='consumo_laboratorio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='esperaexamen',
            name='estado_pago_laboratorio',
            field=models.CharField(choices=[(1, 'Completo'), (2, 'Parcialmente'), (3, 'Pendiente')], default=1, max_length=15),
        ),
        migrations.AlterField(
            model_name='examenlaboratorio',
            name='tipo_muestra',
            field=models.CharField(choices=[('1', 'sangre'), ('2', 'orina'), ('3', 'heces'), ('4', 'tejidos')], max_length=15),
        ),
        migrations.AlterField(
            model_name='resultado',
            name='lic_laboratorio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='modulo_control.liclaboratorioclinico'),
        ),
    ]
