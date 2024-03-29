# Generated by Django 3.2.12 on 2022-10-10 00:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('modulo_laboratorio', '0007_auto_20221010_0031'),
        ('modulo_expediente', '0029_tipoconsulta'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id_servicio', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id_publicidad', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.TextField()),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('cantidad_visitas', models.IntegerField(default=0)),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publicaciones', to='modulo_publicidad.servicio')),
            ],
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id_imagen', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=25)),
                ('publicidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='modulo_publicidad.publicacion')),
            ],
        ),
        migrations.CreateModel(
            name='Descuento',
            fields=[
                ('id_descuento', models.AutoField(primary_key=True, serialize=False)),
                ('codigo_descuento', models.CharField(max_length=15)),
                ('fecha_expedicion', models.DateField(auto_now_add=True)),
                ('fecha_expiracion', models.DateField(null=True)),
                ('cantidad_descuento', models.DecimalField(decimal_places=2, max_digits=10)),
                ('restricciones', models.TextField()),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='descuentos', to='modulo_publicidad.servicio')),
            ],
        ),
        migrations.CreateModel(
            name='ServicioMedico',
            fields=[
                ('servicio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='modulo_publicidad.servicio')),
                ('id_servicio_medico', models.AutoField(primary_key=True, serialize=False)),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicios_medicos', to='modulo_publicidad.servicio')),
                ('tipo_consulta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_expediente.tipoconsulta')),
            ],
            bases=('modulo_publicidad.servicio',),
        ),
        migrations.CreateModel(
            name='ServicioLaboratorioClinico',
            fields=[
                ('servicio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='modulo_publicidad.servicio')),
                ('id_servicio_laboratorio_clinico', models.AutoField(primary_key=True, serialize=False)),
                ('examen_laboratorio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_laboratorio.examenlaboratorio')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicios_laboratorio_clinico', to='modulo_publicidad.servicio')),
            ],
            bases=('modulo_publicidad.servicio',),
        ),
    ]
