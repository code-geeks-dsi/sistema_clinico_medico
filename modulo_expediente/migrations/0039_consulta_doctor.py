# Generated by Django 3.2.12 on 2023-05-14 00:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modulo_expediente', '0038_auto_20221125_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='consulta',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
