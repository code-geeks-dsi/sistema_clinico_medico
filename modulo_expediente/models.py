from argparse import _MutuallyExclusiveGroup
from datetime import datetime
from pyexpat import model
from secrets import choice
from django.db import models
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator


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

class ContieneConsulta(models.Model):
    expediente = models.ManyToManyField(Expediente, models.DO_NOTHING, blank=False, null=True,through='Expediente')
    consulta = models.ManyToManyField(Consulta, models.DO_NOTHING, blank=False, null=True,through='Consulta')

class SignosVitales(models.Model):
    UNIDADES_TEMPERATURA=(
        (1,'F','Fahrenheit'),
        (2,'C','Celsius'),
    )
    UNIDADES_PESO=(
        (1,'Lbs','Libras'),
        (2,'Kgs','Kilogramos'),
    )
    id_signos_vitales= models.AutoField(primary_key=True)
    consulta=models.ForeignKey(Consulta,on_delete=models.DO_NOTHING,null=False, blank=False)
    # enfermera=models.ForeignKey(Enfermera,on_delete=models.DO_NOTHING,null=False, blank=False)
    unidad_temperatura=models.CharField(max_length=1,choices=UNIDADES_TEMPERATURA,null=False, blank=True)
    unidad_peso=models.CharField(max_length=3,choices=UNIDADES_PESO,null=False, blank=True)
    unidad_presion_arterial_diastolica=models.CharField(max_length=4,default='mmHH',null=False, blank=True)
    unidad_presion_arterial_sistolica=models.CharField(max_length=4,default='mmHH',null=False, blank=True)
    unidad_frecuencia_cardiaca=models.CharField(max_length=3,null=False, blank=True)
    unidad_saturacion_oxigeno=models.CharField(max_length=1,default='%',null=False, blank=True)

    valor_temperatura=models.DecimalField(max_digits=5,decimal_places=2,validators=[MaxValueValidator(50),MinValueValidator(15)],null=False, blank=True)
    valor_peso=models.DecimalField(max_digits=4,decimal_places=2,validators=[MaxValueValidator(500),MinValueValidator(0)],null=False, blank=True)
    valor_presion_arterial_diastolica=models.IntegerField(max_length=3,validators=[MaxValueValidator(250),MinValueValidator(0)],null=False, blank=True)
    valor_presion_arterial_sistolica=models.IntegerField(max_length=3,validators=[MaxValueValidator(350),MinValueValidator(0)],null=False, blank=True)
    valor_frecuencia_cardiaca=models.IntegerField(max_length=3,validators=[MaxValueValidator(250),MinValueValidator(0)],null=False, blank=True)
    valor_saturacion_oxigeno=models.IntegerField(max_length=3,validators=[MaxValueValidator(101),MinValueValidator(0)],null=False, blank=True)


class OrdenExamenLaboratorio(models.Model):
    id_orden_examen_laboratorio= models.AutoField(primary_key=True)
    fecha_programada=models.DateField(default=datetime.now,null=False, blank=False)
    # examen_de_laboratorio=models.ForeignKey(ExamenDeLaboratorio,,on_delete=models.DO_NOTHING,null=False, blank=False)


class Hospital(models.Model):
    id_hospital= models.AutoField(primary_key=True)
    codigo_hospital=models.CharField(max_length=25)
    nombre_hospital=models.CharField(max_length=50)
    telefono_hospital=models.CharField(max_length=9)
    codigo_pais=models.CharField(max_length=3)

class ReferenciaMedica(models.Model):
    id_referencia_medica= models.AutoField(primary_key=True)
    hospital=models.ForeignKey(Hospital,models.DO_NOTHING,null=False, blank=False)
    especialidad=models.CharField(max_length=30,null=False, blank=False)
    fecha_referencia=models.DateField(default=datetime.now,null=False, blank=False)



class RecetaMedica(models.Model):
    id_receta_medica= models.AutoField(primary_key=True)

class Medicamento(models.Model):
    UNIDADES_DE_MEDIDA_MEDICAMENTO=(
    (3,'L','litro'),
    (4,'mL','mililitro'),
    (5,'µL','microlitro'),
    (6,'cc / cm³','centímetro cúbico'),
    (7,'fl oz',	'onza líquida'),
    (10,'Kg','kilogramo'),
    (11,'g','gramo'),
    (12,'mg','miligramo'),
    (13,'oz','onza'),
    (15,'capsulas','cápsulas'),
    )
    id_medicamento= models.AutoField(primary_key=True)
    nombre_comercial=models.CharField(max_length=50,null=False, blank=False)
    nombre_generico=models.CharField(max_length=25,null=False, blank=False)
    cantidad_medicamento=models.DecimalField(max_digits=6,decimal_places=2,null=False, blank=False)
    unidad_medicamento=models.CharField(max_length=8,choices=UNIDADES_DE_MEDIDA_MEDICAMENTO,null=False, blank=False)

class Dosis(models.Model):
    OPCIONES_TIEMPO = (
        (1, 'Hora(s)'),
        (2, 'Dia(s)'),
        (3, 'Semana(s)'),
        (4, 'Mes(es)'),
    )
    UNIDADES_DE_MEDIDA_DOSIS=(
    (1,'got',	'gota'),
    (2,'mgota / µgota'	'microgota')
    (3,'L',	'litro'),
    (4,'mL',	'mililitro'),
    (5,'µL',	'microlitro'),
    (6,'cc / cm³',	'centímetro cúbico'),
    (7,'fl oz',	'onza líquida'),
    (8,'cdita',	'cucharadita'),
    (9,'cda',	'cucharada'),
    (10,'Kg',	'kilogramo'),
    (11,'g',	'gramo'),
    (12,'mg',	'miligramo'),
    (13,'oz',	'onza'),
    (14,'disparos'	,'disparos'),
    (15,'capsulas',	'cápsulas'),
    )
    id_dosis= models.AutoField(primary_key=True)
    periodo_dosis=models.IntegerField(max_length=2,null=False,Blank=False)
    unidad_periodo_dosis=models.CharField(max_length=6,choices=OPCIONES_TIEMPO,null=False,blank=False)
    frecuencia_dosis=models.IntegerField(max_length=2,null=False,Blank=False)
    unidad_frecuencia_dosis=models.CharField(max_length=6,choices=OPCIONES_TIEMPO,null=False,blank=False)
    cantidad_dosis=models.DecimalField(decimal_places=2,max_digits=5,null=False,Blank=False)
    unidad_de_medida_dosis=models.CharField(chocices=UNIDADES_DE_MEDIDA_DOSIS,max_length=17,null=False,Blank=False)
    medicamento=models.OneToOneField(Medicamento,on_delete=models.DO_NOTHING,parent_link=True,null=False, blank=False)
    receta_medica=models.ForeignKey(RecetaMedica,on_delete=models.DO_NOTHING,null=False, blank=False)



class ConstanciaMedica(models.Model):
    id_constancia_medica= models.AutoField(primary_key=True)

