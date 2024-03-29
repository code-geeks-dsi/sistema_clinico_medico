# Generated by Django 3.2.12 on 2022-08-10 07:44

from django.db import migrations, models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_expediente', '0004_constanciamedica_acompanante'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archivo',
            fields=[
                ('id_archivo', models.AutoField(primary_key=True, serialize=False)),
                ('archivo', models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='isai-medico-test'), upload_to='exams')),
            ],
        ),
    ]
