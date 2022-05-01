from msilib.schema import Class
from pyexpat import model
from tkinter import CASCADE
from turtle import back
from django.db import models
from django.forms import DateField

# Create your models here.

class EsperaExamen(models.Model):
    OPCIONES_ESTADO=(
        (1, 'Completo'),
        (2, 'Parcialmente')
        (3, 'Pendiente')
    )
    resultado=models.ForeignKey('Resultado', on_delete=models.CASCADE)
    paciente=models.ForeignKey('modulo_expediente_Paciente', on_delete=models.CASCADE)
    estado_pago_laboratorio=models.CharField(max_length=15, default="-", choices=OPCIONES_ESTADO, null=False, blank=False)
    numero_cola_laboratorio=models.IntegerField(null=False,blank=False)
    consumo_laboratorio=models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return str(self.id_examina)+" - "+str(self.id_paciente)

class Resultado(models.Model):
    id_resultado = models.AutoField(primary_key=True)
    lic_laboratorio = models.ForeignKey('modulo_control.LicLaboratorioClinico', on_delete=CASCADE)
    paciente = models.ForeignKey('modulo_expediente.Paciente', on_delete=models.CASCADE)
    parametro=models.ManyToManyField('Parametro', through='ContieneValor')
    fecha_resultado=models.DateField()

    def __str__(self):
        return self.id_resultado

class ContieneValor(models.Model):
    resultado = models.ForeignKey('Resultado', on_delete=CASCADE)
    parametro = models.ForeignKey('Parametro', on_delete=CASCADE)
    dato=models.DecimalField(max_digits=12, decimal_places=3, null=False,blank=False)

    def __str__(self):
        return self.id_resultado


