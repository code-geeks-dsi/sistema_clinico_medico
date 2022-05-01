from django.db import models

# Create your models here.
class Parametro(models.model):
id_parametro = models.AutoField(primary_key=True)
nombre_parametro = models.CharField(,max_length=40,null=false, blank=false)
unidad_parametro = models.CharField(, max_length=40, null=True,blank=false)

