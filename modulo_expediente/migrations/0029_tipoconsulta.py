# Generated by Django 3.2.12 on 2022-10-10 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_expediente', '0028_alter_recetaordenexamenlaboratorioitem_examen'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoConsulta',
            fields=[
                ('id_tipo_consulta', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(choices=[('G', 'General'), ('CP', 'Control Prenatal'), ('CNS', 'Control Niño Sano'), ('CAM', 'Control Adulto Mayor')], default='G', max_length=3)),
            ],
        ),
    ]