from django.db import models

# Create your models here.
class Parametro(models.model):
    id_parametro = models.AutoField
    nombre_parametro = models.CharField(,max_length=40,null=false, blank=false)
    unidad_parametro = models.CharField(, max_length=40, null=True,blank=false)

class ServicioDeLaboratorioClinico(models.model)
    id_servicio =models.AutoField(primary_key=True)
    precio_servicio_clinica=models.DecimalField(max_digits=10,decimal_places=2,null=False, blank=False)
