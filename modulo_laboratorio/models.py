from datetime import datetime
from platform import mac_ver
from pydoc import describe
from re import S
from unittest import result
from django.db import models
from django.forms import DateField
from django.utils.timezone import now
from modulo_expediente.models import Expediente, Paciente


# Create your models here.

class EsperaExamen(models.Model):
    OPCIONES_ESTADO=(
        ('1', 'Cancelado'),
        ('3', 'Pendiente')
    )
    OPCIONES_FASE_ORDEN=(
        ('RC','Recepcion'),
        ('EP','En Proceso'),
        ('RE','Resultados Entregado'),
        ('PF','Proceso Finalizado')
    )
    expediente=models.ForeignKey('modulo_expediente.Expediente', on_delete=models.CASCADE)
    estado_pago_laboratorio=models.CharField(max_length=15, default=OPCIONES_ESTADO[1][0], choices=OPCIONES_ESTADO, null=False, blank=False)
    numero_cola_orden=models.IntegerField(null=False,blank=False)
    fase_examenes_lab=models.CharField(max_length=2,choices=OPCIONES_FASE_ORDEN, blank=False,null=False,default=OPCIONES_FASE_ORDEN[0][0])
    fecha=models.DateTimeField( default=now, blank=True)

    @classmethod
    def create(cls, id_paciente,id_examen_laboratorio):
        expediente=Expediente.objects.get(id_paciente=id_paciente)
        examen_laboratorio=ExamenLaboratorio.objects.get(id_examen_laboratorio=id_examen_laboratorio)
        hoy=datetime.now()
        try:
            numero_cola_laboratorio=EsperaExamen.objects.filter(
                                fecha__year=hoy.year, 
                                fecha__month=hoy.month).last().numero_cola_laboratorio+1
        except:
            numero_cola_laboratorio=1
        cola_item = cls(
            expediente=expediente,
            numero_cola_laboratorio=numero_cola_laboratorio)
            
        return cola_item
    def __str__(self):
        return str(self.get_fase_examenes_lab_display())+" - "+str(self.expediente.id_paciente.nombre_paciente)

class Resultado(models.Model):
    OPCIONES_FASE=(
        ('1','Recepción de muestra'),
        ('2','Resultados en Proceso'),
        ('3','Resultados Listos')
    )
    id_resultado = models.AutoField(primary_key=True)
    lic_laboratorio = models.ForeignKey('modulo_control.LicLaboratorioClinico', on_delete=models.CASCADE,null=True)
    examen_laboratorio= models.ForeignKey('ExamenLaboratorio', on_delete=models.CASCADE,null=False)
    fase_examenes_lab=models.CharField(max_length=25,choices=OPCIONES_FASE, blank=False,null=False,default=OPCIONES_FASE[0][0])
    numero_cola_resultado=models.IntegerField(null=False,blank=False)
    observaciones=models.TextField(null=False,blank=True,default="")
    fecha_hora_toma_de_muestra=models.DateTimeField(null=True,blank=True)
    fecha_hora_elaboracion_de_reporte=models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.examen_laboratorio.nombre_examen

class ContieneValor(models.Model):
    resultado = models.ForeignKey('Resultado', on_delete=models.CASCADE)
    parametro = models.ForeignKey('Parametro', on_delete=models.CASCADE)
    dato=models.DecimalField(max_digits=12, decimal_places=3, null=False,blank=False,default=0)
    class Meta:
        unique_together = ('resultado', 'parametro',)
    def __str__(self):
        return self.parametro.nombre_parametro+": "+str(self.dato)+" "+self.parametro.unidad_parametro

class ExamenLaboratorio(models.Model):
    OPCIONES_MUESTRA=(
        ('NA',''),
        ('1', 'sangre'),
        ('2', 'orina'),
        ('3', 'heces'),
        ('4', 'tejidos'),
    )
    OPCIONES_RESULTADO=(
        ('NA',''),
        ('P','POSITIVO'),
        ('N','NEGATIVO'),
        ('NAF','NEGATIVO A LA FECHA'),
        ('R','REACTIVO'),
        ('NR','NO REACTIVO'),
        ('NRAF','NO REACTIVO A LA FECHA'),
    )
    id_examen_laboratorio=models.AutoField(primary_key=True)
    categoria=models.ManyToManyField('Categoria', through='CategoriaExamen')
    nombre_examen=models.CharField(max_length=40, null=False,blank=False) #tipo_examen
    tipo_muestra=models.CharField(max_length=15,choices=OPCIONES_MUESTRA ,null=False,blank=True,default=OPCIONES_MUESTRA[0][0])
    nota=models.CharField(null=False,blank=True,default="",max_length=100)
    
    def __str__(self):
        return self.nombre_examen


class CategoriaExamen(models.Model):
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    examen_laboratorio=models.ForeignKey('ExamenLaboratorio', on_delete=models.CASCADE)

    def __str__(self):
        return self.categoria.descripcion_categoria +" "+ self.examen_laboratorio.nombre_examen
    

class Categoria(models.Model):
    id_categoria=models.AutoField(primary_key=True)
    # nombre_categoria=models.CharField(max_length=30, null=False,blank=False)
    descripcion_categoria=models.CharField(max_length=40, null=True,blank=True)

    def __str__(self):
        return self.descripcion_categoria


class Parametro(models.Model):
    id_parametro = models.AutoField(primary_key=True)
    nombre_parametro = models.CharField(max_length=40,null=False, blank=False)
    unidad_parametro = models.CharField(max_length=40, null=True,blank=True)
    examen_de_laboratorio = models.ForeignKey('ExamenLaboratorio', models.CASCADE, blank=False, null=True)
    valor_por_defecto=models.CharField( null=True,blank=True,default="",max_length=10)

    def __str__(self):
        return self.nombre_parametro + " "+self.examen_de_laboratorio.nombre_examen

class RangoDeReferencia(models.Model):
    id_rango_referencia=models.AutoField(primary_key=True)
    parametro= models.ForeignKey('Parametro', models.CASCADE, blank=False, null=False)
    descripcion=models.CharField(null=False,blank=True,default="",max_length=75)
    valor_maximo=models.CharField(null=True,blank=True,max_length=15)
    valor_minimo=models.CharField(null=True,blank=True,max_length=15)
    valor=models.CharField(null=True,blank=True,max_length=15)
    unidad=models.CharField(null=False,blank=True,default="",max_length=8)
    def __str__(self):
        return self.parametro.nombre_parametro+" "+self.descripcion


