from datetime import datetime
from pyexpat import model
from turtle import mode
from django.db import models

# Create your models here.
class Paciente(models.Model):
    OPCIONES_SEXO=(
        (1, 'Masculino'),
        (2, 'Femenino'),
    )
    id_paciente=models.AutoField(primary_key=True,unique=True)
    nombre_paciente = models.CharField( max_length=40,blank=False, null=False)
    apellido_paciente = models.CharField( max_length=40,blank=False, null=False)
    fecha_nacimiento_paciente = models.DateField( blank=False,null=False)
    sexo_paciente = models.CharField( max_length=1,choices=OPCIONES_SEXO, blank=False, null=False )
    direccion_paciente=models.CharField( max_length=120, blank=False,null=False)
    email_paciente = models.EmailField( max_length=100, blank=False, null=False, unique=True)
    responsable=models.CharField(max_length=40,blank=False,null=False)


class Expediente (models.Model):
    id_expediente= models.AutoField(primary_key=True, max_length=8,null=False, blank=False)
  

class Consulta(models.Model):
    id_consulta= models.AutoField(primary_key=True)
    constancia_medica= models.OneToOneField(ConstanciaMedica,on_delete=models.DO_NOTHING,parent_link=True,null=False, blank=False)
    signos_vitales= models.OneToOneField(SignosVitales,on_delete=models.DO_NOTHING,parent_link=True,null=False, blank=False)
    examen_de_laboratorio= models.OneToOneField(OrdenExamenLaboratorio, on_delete=models.DO_NOTHING, blank=False, null=False)
    diagnostico=models.CharField(max_length=200, blank=False, null=False)
    sintoma=models.CharField(max_length=200, blank=False, null=False)

class ContieneConsulta(models.Model):
    OPCIONES_ESTADO_DE_PAGO=(
        (1,'No pagado'),
        (2,'Parcialmente pagado'),
        (3,'Pagado'),
    )
    OPCIONES_FASE=(
        (1,'Agendado'),
        (2,'Agregar a cola'),
        (3,'Anotado'),
        (4,'Preparado'),
        (5,'En espera'),
        (6,'En consulta'),
        (7,'Atender paciente'),
        (8,'Ver expediente'),
        (9,'Finalizar consulta'),
    )
    expediente = models.ManyToManyField(Expediente, models.DO_NOTHING, blank=False, null=True)
    consulta = models.ManyToManyField(Consulta, models.DO_NOTHING, blank=False, null=True)
    numero_cola=models.IntegerField(max_length=6, blank=False, null=False)
    fecha_de_cola=models.DateField(default=datetime.now, blank=False, null=False)
    consumo_medico=models.DecimalField(max_digits=6,decimal_places=2,null=False, blank=False)
    estado_cola_medica=models.CharField(max_length=20,choices=OPCIONES_ESTADO_DE_PAGO, blank=False,null=False)
    fase_cola_medica=models.CharField(max_length=20,choices=OPCIONES_FASE, blank=False,null=False)

class SignosVitales(models.Model):
    id_signos_vitales= models.AutoField(primary_key=True)

class OrdenExamenLaboratorio(models.Model):
    id_orden_examen_laboratorio= models.AutoField(primary_key=True)

class ReferenciaMedica(models.Model):
    id_referencia_medica= models.AutoField(primary_key=True)

class Hospital(models.Model):
    id_hospital= models.AutoField(primary_key=True)

class Receta_Medica(models.Model):
    id_receta_medica= models.AutoField(primary_key=True)

class Dosis(models.Model):
    id_dosis= models.AutoField(primary_key=True)

class Medicamento(models.Model):
    id_medicamento= models.AutoField(primary_key=True)

class BrindaConsulta(models.Model):
    OPCIONES_TURNO=(
        (1,'Matutino'),
        (2,'Vespertino'),
    )
    consulta=models.ForeignKey(Consulta, models.DO_NOTHING, blank=False, null=False)
    doctor=models.ForeignKey(Doctor, models.DO_NOTHING, blank=False, null=False)
    consultorio=models.IntegerField(max_length=2, blank=False, null=False)
    turno=models.CharField(max_length=20,choices=OPCIONES_FASE, blank=False,null=False)

class ConstanciaMedica(models.Model):
    id_constancia_medica= models.AutoField(primary_key=True)
    consulta= models.ForeignKey(Consulta, models.DO_NOTHING, blank=False, null=False)
    fecha_de_emision=models.DateField(default=datetime.now, blank=False, null=False)
    dias_reposo=models.IntegerField(max_length=2, blank=False, null=False)
    diagnostico_constancia=models.CharField(max_length=200, blank=False, null=False)


