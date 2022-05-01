from argparse import _MutuallyExclusiveGroup
from pyexpat import model
from django.db import models

# Create your models here.

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
    id_signos_vitales= models.AutoField(primary_key=True)

class OrdenExamenLaboratorio(models.Model):
    id_orden_examen_laboratorio= models.AutoField(primary_key=True)

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
    fecha_referencia=models.DateField(auto_now_add=True,null=False, blank=False)



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

