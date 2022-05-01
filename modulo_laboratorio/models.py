from django.db import models

# Create your models here.
class Parametro(AbstractBaseUser, PermissionsMixin):
nombre_parametro = models.CharField(db_column='UNIDAD',max_length=40,unique=True)
unidad_parametro = models.CharField(db_column='UNIDAD', max_length=40, null=True)

