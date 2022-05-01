from django.db import models

# Create your models here.
class Parametro(models.model):
    id_parametro = models.AutoField
    nombre_parametro = models.CharField(,max_length=40,null=false, blank=false)
    unidad_parametro = models.CharField(, max_length=40, null=True,blank=false)
    examen_de_laboratorio = models.ForeignKey(examen_de_laboratorio, models.DO_NOTHING, blank=False, null=True)

class ServicioDeLaboratorioClinico(models.model)
    id_servicio =models.AutoField(primary_key=True)
    precio_servicio_clinica=models.DecimalField(max_digits=10,decimal_places=2,null=False, blank=False)
    examen_de_laboratorio=models.OneToOneField(examen_de_laboratorio,model.DO_NOTHING,blank=false,null=false,through='examen_de_laboratorio')
