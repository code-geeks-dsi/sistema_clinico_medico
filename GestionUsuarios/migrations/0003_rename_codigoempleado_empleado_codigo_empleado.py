# Generated by Django 3.2.12 on 2022-05-01 00:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GestionUsuarios', '0002_rename_codigo_empleado_empleado_codigoempleado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='empleado',
            old_name='codigoEmpleado',
            new_name='codigo_empleado',
        ),
    ]