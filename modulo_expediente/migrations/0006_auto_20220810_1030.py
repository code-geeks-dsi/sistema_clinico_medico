# Generated by Django 3.2.12 on 2022-08-10 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_expediente', '0005_archivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='expediente',
            name='antecedentes_familiares',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='expediente',
            name='antecedentes_personales',
            field=models.TextField(blank=True, null=True),
        ),
    ]
