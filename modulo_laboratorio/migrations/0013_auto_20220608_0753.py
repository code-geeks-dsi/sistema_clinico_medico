# Generated by Django 3.2.12 on 2022-06-08 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_laboratorio', '0012_auto_20220608_0745'),
    ]

    operations = [
        migrations.AddField(
            model_name='rangodereferencia',
            name='valor',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='unidad_parametro',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]