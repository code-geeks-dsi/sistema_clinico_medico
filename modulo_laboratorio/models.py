from django.db import models

# Create your models here.
class Parametro(AbstractBaseUser, PermissionsMixin):
id_parametro = models.AutoField(primary_key=True)
nombre_parametro = models.CharField(db_column='NOMBRE_PARAMETRO',max_length=40,unique=True)
unidad_parametro = models.CharField(db_column='UNIDAD_PARAMETRO', max_length=40, null=True)

