from django.db import models
from django.forms import DateField


# Create your models here.

class EsperaExamen(models.Model):
    OPCIONES_ESTADO=(
        (1, 'Completo'),
        (2, 'Parcialmente'),
        (3, 'Pendiente')
    )
    resultado=models.ForeignKey('Resultado', on_delete=models.CASCADE)
    paciente=models.ForeignKey('modulo_expediente.Paciente', on_delete=models.CASCADE)
    estado_pago_laboratorio=models.CharField(max_length=15, default="-", choices=OPCIONES_ESTADO, null=False, blank=False)
    numero_cola_laboratorio=models.IntegerField(null=False,blank=False)
    consumo_laboratorio=models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return str(self.id_examina)+" - "+str(self.id_paciente)

class Resultado(models.Model):
    id_resultado = models.AutoField(primary_key=True)
    lic_laboratorio = models.ForeignKey('modulo_control.LicLaboratorioClinico', on_delete=models.CASCADE)
    paciente = models.ForeignKey('modulo_expediente.Paciente', on_delete=models.CASCADE)
    parametro=models.ManyToManyField('Parametro', through='ContieneValor')
    fecha_resultado=models.DateField()

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
        (1, 'sangre'),
        (2, 'orina'),
        (3, 'heces'),
        (4, 'tejidos'),
    )
    id_examen_laboratorio=models.AutoField(primary_key=True)
    categoria=models.ManyToManyField('Categoria', through='CategoriaExamen')
    codigo_examen=models.CharField(max_length=8, null=False, blank=False)
    nombre_examen=models.CharField(max_length=40, null=False,blank=False) #tipo_examen
    tipo_muestra=models.CharField(max_length=15,choices=OPCIONES_MUESTRA ,null=False,blank=False)

class CategoriaExamen(models.Model):
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    examen_laboratorio=models.ForeignKey('ExamenLaboratorio', on_delete=models.CASCADE)

class Categoria(models.Model):
    id_categoria=models.AutoField(primary_key=True)
    nombre_categoria=models.CharField(max_length=30, null=False,blank=False)
    descripcion_categoria=models.CharField(max_length=40, null=True,blank=True)

class Parametro(models.Model):
    id_parametro = models.AutoField(primary_key=True)
    nombre_parametro = models.CharField(max_length=40,null=False, blank=False)
    unidad_parametro = models.CharField(max_length=40, null=True,blank=False)
    examen_de_laboratorio = models.ForeignKey('ExamenLaboratorio', models.DO_NOTHING, blank=False, null=True)

class ServicioDeLaboratorioClinico(models.Model):
    id_servicio =models.AutoField(primary_key=True)
    precio_servicio_clinica=models.DecimalField(max_digits=10,decimal_places=2,null=False, blank=False)
    examen_de_laboratorio=models.ForeignKey('ExamenLaboratorio',on_delete=models.CASCADE,blank=False,null=False)



