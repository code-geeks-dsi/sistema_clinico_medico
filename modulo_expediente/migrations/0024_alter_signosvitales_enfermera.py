# Generated by Django 3.2.12 on 2022-07-29 07:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modulo_expediente', '0023_auto_20220607_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signosvitales',
            name='enfermera',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]