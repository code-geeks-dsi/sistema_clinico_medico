from datetime import datetime
from re import S
from unittest import result
from django.db import models
from django.forms import DateField
from django.utils.timezone import now
from modulo_expediente.models import Expediente, Paciente


# Create your models here.

class EsperaExamen(models.Model):
    OPCIONES_ESTADO=(
        (1, 'Completo'),
        (2, 'Parcialmente'),
        (3, 'Pendiente')
    )
    OPCIONES_FASE=(
        ('1','Preparado'),
        ('2','Finalizado'),
    )
    resultado=models.ForeignKey('Resultado', on_delete=models.CASCADE)
    expediente=models.ForeignKey('modulo_expediente.Expediente', on_delete=models.CASCADE)
    estado_pago_laboratorio=models.CharField(max_length=15, default=OPCIONES_ESTADO[0][0], choices=OPCIONES_ESTADO, null=False, blank=False)
    numero_cola_laboratorio=models.IntegerField(null=False,blank=False)
    consumo_laboratorio=models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False,default=0)
    fase_examenes_lab=models.CharField(max_length=20,choices=OPCIONES_FASE, blank=False,null=False,default=OPCIONES_FASE[0][0])
    fecha=models.DateTimeField( default=now, blank=True)

    @classmethod
    def create(cls, id_paciente,id_examen_laboratorio):
        expediente=Expediente.objects.get(id_paciente=id_paciente)
        examen_laboratorio=ExamenLaboratorio.objects.get(id_examen_laboratorio=id_examen_laboratorio)
        resultado=Resultado(examen_laboratorio=examen_laboratorio)
        resultado.save()
        hoy=datetime.now()
        try:
            numero_cola_laboratorio=EsperaExamen.objects.filter(
                                fecha__year=hoy.year, 
                                fecha__month=hoy.month).last().numero_cola_laboratorio+1
        except:
            numero_cola_laboratorio=1
        cola_item = cls(
            expediente=expediente,
            resultado=resultado,
            numero_cola_laboratorio=numero_cola_laboratorio)
            
        return cola_item
    def __str__(self):
        return str(self.id_examina)+" - "+str(self.id_paciente)

class Resultado(models.Model):
    id_resultado = models.AutoField(primary_key=True)
    lic_laboratorio = models.ForeignKey('modulo_control.LicLaboratorioClinico', on_delete=models.CASCADE,null=True)
    examen_laboratorio= models.ForeignKey('ExamenLaboratorio', on_delete=models.DO_NOTHING,null=False)
    

    def __str__(self):
        return self.id_resultado

class ContieneValor(models.Model):
    resultado = models.ForeignKey('Resultado', on_delete=models.CASCADE)
    parametro = models.ForeignKey('Parametro', on_delete=models.CASCADE)
    dato=models.DecimalField(max_digits=12, decimal_places=3, null=False,blank=False)

    def __str__(self):
        return self.id_resultado

class ExamenLaboratorio(models.Model):
    OPCIONES_MUESTRA=(
        ('1', 'sangre'),
        ('2', 'orina'),
        ('3', 'heces'),
        ('4', 'tejidos'),
    )
    id_examen_laboratorio=models.AutoField(primary_key=True)
    categoria=models.ManyToManyField('Categoria', through='CategoriaExamen')
    codigo_examen=models.CharField(max_length=8, null=False, blank=False)
    nombre_examen=models.CharField(max_length=40, null=False,blank=False) #tipo_examen
    tipo_muestra=models.CharField(max_length=15,choices=OPCIONES_MUESTRA ,null=False,blank=False)
    def __str__(self):
        return self.nombre_examen


class CategoriaExamen(models.Model):
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    examen_laboratorio=models.ForeignKey('ExamenLaboratorio', on_delete=models.CASCADE)

    def __str__(self):
        return self.categoria.nombre_categoria +" "+ self.examen_laboratorio.nombre_examen
    

class Categoria(models.Model):
    id_categoria=models.AutoField(primary_key=True)
    nombre_categoria=models.CharField(max_length=30, null=False,blank=False)
    descripcion_categoria=models.CharField(max_length=40, null=True,blank=True)

    def __str__(self):
        return self.nombre_categoria


class Parametro(models.Model):
    id_parametro = models.AutoField(primary_key=True)
    nombre_parametro = models.CharField(max_length=40,null=False, blank=False)
    unidad_parametro = models.CharField(max_length=40, null=True,blank=False)
    examen_de_laboratorio = models.ForeignKey('ExamenLaboratorio', models.DO_NOTHING, blank=False, null=True)

    def __str__(self):
        return self.nombre_parametro + " "+self.examen_de_laboratorio.nombre_examen

class ServicioDeLaboratorioClinico(models.Model):
    id_servicio =models.AutoField(primary_key=True)
    precio_servicio_clinica=models.DecimalField(max_digits=10,decimal_places=2,null=False, blank=False)
    examen_de_laboratorio=models.ForeignKey('ExamenLaboratorio',on_delete=models.CASCADE,blank=False,null=False)



