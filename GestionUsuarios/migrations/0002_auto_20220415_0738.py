# Generated by Django 3.2.12 on 2022-04-15 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionUsuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='es_activo',
            field=models.BooleanField(db_column='ES_ACTIVE', default=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='es_staff',
            field=models.BooleanField(db_column='ES_STAFF', default=False),
        ),
    ]