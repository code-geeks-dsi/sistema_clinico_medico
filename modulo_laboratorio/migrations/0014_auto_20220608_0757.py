# Generated by Django 3.2.12 on 2022-06-08 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_laboratorio', '0013_auto_20220608_0753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rangodereferencia',
            name='valor',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='rangodereferencia',
            name='valor_maximo',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='rangodereferencia',
            name='valor_minimo',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
