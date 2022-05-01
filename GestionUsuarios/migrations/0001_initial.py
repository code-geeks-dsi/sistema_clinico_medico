# Generated by Django 3.2.12 on 2022-05-01 00:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('codigo_empleado', models.CharField(max_length=7, primary_key=True, serialize=False, unique=True)),
                ('nombres', models.CharField(db_column='NOMBRES', max_length=40, null=True)),
                ('apellidos', models.CharField(db_column='APELLIDOS', max_length=40, null=True)),
                ('sexo', models.CharField(db_column='SEXO', default='-', max_length=1)),
                ('direccion', models.CharField(db_column='DIRECCION', max_length=120, null=True)),
                ('email', models.EmailField(blank=True, db_column='EMAIL', max_length=100, null=True, unique=True)),
                ('es_activo', models.BooleanField(db_column='ES_ACTIVO', default=True)),
                ('es_staff', models.BooleanField(db_column='ES_STAFF', default=False)),
                ('es_superuser', models.BooleanField(db_column='IS_SUPERUSER', default=False)),
                ('last_login', models.DateField(db_column='LAST_LOGIN', null=True)),
                ('fechaCreacion', models.DateTimeField(db_column='FECHA_CREACION', default=django.utils.timezone.now)),
                ('fechaNacimiento', models.DateField(db_column='FECHA_NACMIENTO', null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
