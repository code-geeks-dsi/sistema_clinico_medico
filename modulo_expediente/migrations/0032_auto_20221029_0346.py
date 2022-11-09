# Generated by Django 3.2.12 on 2022-10-29 03:46

from django.db import migrations

def postgres_migration_prep(apps, schema_editor):
    signoVital = apps.get_model("modulo_expediente", "SignosVitales")
    fields = ("valor_frecuencia_cardiaca", "valor_peso", "valor_presion_arterial_diastolica",
    "valor_presion_arterial_sistolica", "valor_saturacion_oxigeno", "valor_temperatura",
    )

    for field in fields:
        filter_param = {"{}__isnull".format(field): True}
        update_param = {field: 0}
        signoVital.objects.filter(**filter_param).update(**update_param)

class Migration(migrations.Migration):

    dependencies = [
        ('modulo_expediente', '0031_auto_20221028_1609'),
    ]

    operations = [
        migrations.RunPython(postgres_migration_prep, migrations.RunPython.noop)
    ]
