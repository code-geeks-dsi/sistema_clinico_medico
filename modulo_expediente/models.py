from pyexpat import model
from django.db import models


# Create your models here.
class Paciente(models.Model):
    OPCIONES_SEXO=(
        (1, 'Masculino'),
        (2, 'Femenino'),
    )
    id_paciente=models.AutoField(primary_key=True,unique=True)
    id_expediente=models.ForeignKey(Expediente, models.DO_NOTHING, blank=False, null=False)
    nombre_paciente = models.CharField( max_length=40,blank=False, null=False)
    apellido_paciente = models.CharField( max_length=40,blank=False, null=False)
    fecha_nacimiento_paciente = models.DateField( blank=False,null=False)
    sexo_paciente = models.CharField( max_length=1,choices=OPCIONES_SEXO, blank=False, null=False )
    direccion_paciente=models.CharField( max_length=120, blank=False,null=False)
    email_paciente = models.EmailField( max_length=100, blank=False, null=False, unique=True)
    responsable=models.CharField(max_length=40,blank=False,null=False)

class Expediente(models.model)
    
    id_expediente = models.AutoField(primary_key=True, unique=True)
    fecha_creacion_expediente = models.DateField(default=datetime.now,blank=false,null=false)
    codigo_expediente=models.CharField(max_length=10,blank=false,null=false,unique=True)
    contiene_consulta=models.ManyToManyField(contiene_consulta,model.DO_NOTHING,blank=false,null=false,through='contiene_consulta')

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

