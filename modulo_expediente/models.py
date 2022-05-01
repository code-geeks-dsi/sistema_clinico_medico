from pyexpat import model
from django.db import models

# Create your models here.

class Paciente(models.Model):
    id_paciente= models.AutoField(primary_key=True)

class Expediente (models.Model):
    id_expediente= models.AutoField(primary_key=True)

class Consulta(models.Model):
    id_consulta= models.AutoField(primary_key=True)

class contiene_consulta(models.Model):
    id_expediente = models.ForeignKey(Expediente, models.DO_NOTHING, blank=False, null=True)
    id_consulta = models.ForeignKey(Consulta, models.DO_NOTHING, blank=False, null=True)

class Signos_Vitales(models.Model):
    id_signos_vitales= models.AutoField(primary_key=True)

class Orden_Examen_Laboratorio(models.Model):
    id_orden_examen_laboratorio= models.AutoField(primary_key=True)

class Referencia_Medica(models.Model):
    id_referencia_medica= models.AutoField(primary_key=True)

class Hospital(models.Model):
    id_hospital= models.AutoField(primary_key=True)

class Receta_Medica(models.Model):
    id_receta_medica= models.AutoField(primary_key=True)

class Dosis(models.Model):
    id_dosis= models.AutoField(primary_key=True)

class Medicamento(models.Model):
    id_medicamento= models.AutoField(primary_key=True)

class Constancia_Medica(models.Model):
    id_constancia_medica= models.AutoField(primary_key=True)

