# Generated by Django 3.2.12 on 2022-08-02 04:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('modulo_expediente', '0001_initial'),
        ('modulo_laboratorio', '0001_initial'),
        ('modulo_control', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordenexamenlaboratorio',
            name='examen_de_laboratorio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='modulo_laboratorio.examenlaboratorio'),
        ),
        migrations.AddField(
            model_name='expediente',
            name='contiene_consulta',
            field=models.ManyToManyField(through='modulo_expediente.ContieneConsulta', to='modulo_expediente.Consulta'),
        ),
        migrations.AddField(
            model_name='expediente',
            name='id_paciente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='modulo_expediente.paciente'),
        ),
        migrations.AddField(
            model_name='evolucionconsulta',
            name='consulta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_expediente.consulta'),
        ),
        migrations.AddField(
            model_name='dosis',
            name='medicamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='modulo_expediente.medicamento'),
        ),
        migrations.AddField(
            model_name='dosis',
            name='receta_medica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='modulo_expediente.recetamedica'),
        ),
        migrations.AddField(
            model_name='controlsubsecuente',
            name='consulta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_expediente.consulta'),
        ),
        migrations.AddField(
            model_name='contieneconsulta',
            name='consulta',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='modulo_expediente.consulta'),
        ),
        migrations.AddField(
            model_name='contieneconsulta',
            name='expediente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='modulo_expediente.expediente'),
        ),
        migrations.AddField(
            model_name='constanciamedica',
            name='consulta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='modulo_expediente.consulta'),
        ),
        migrations.AddField(
            model_name='brindaconsulta',
            name='consulta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='modulo_expediente.consulta'),
        ),
        migrations.AddField(
            model_name='brindaconsulta',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='modulo_control.doctor'),
        ),
        migrations.AlterUniqueTogether(
            name='dosis',
            unique_together={('medicamento', 'receta_medica')},
        ),
        migrations.AlterUniqueTogether(
            name='contieneconsulta',
            unique_together={('expediente', 'fecha_de_cola')},
        ),
    ]
