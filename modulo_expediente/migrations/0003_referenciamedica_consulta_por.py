# Generated by Django 3.2.12 on 2022-08-02 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_expediente', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='referenciamedica',
            name='consulta_por',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]
