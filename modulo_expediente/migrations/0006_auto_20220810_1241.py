# Generated by Django 3.2.12 on 2022-08-10 18:41

from django.db import migrations, models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_expediente', '0006_auto_20220810_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivo',
            name='archivo_publico',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='isai-medico-test', default_acl='public-read'), upload_to='exams'),
        ),
        migrations.AlterField(
            model_name='archivo',
            name='archivo',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket_name='isai-medico-test', default_acl=None), upload_to='exams'),
        ),
    ]
