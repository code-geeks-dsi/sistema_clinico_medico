from cgitb import text
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import datetime

class UsuarioManager(BaseUserManager):
    def create_user(self, primerNombre,segundoNombre,email,primerApellido, segundoApellido,password = None):
        if not email:
            raise ValueError('El Usuario debe tener un correo')
        
        #Codigo Usuario 
        year=datetime.datetime.now().date().strftime("%Y")[2:]
        texto=primerApellido[0]+segundoApellido[0]
        texto=texto.lower()#Solo texto en minusculas
        tamaño=len(Usuario.objects.filter(codigoUsuario__startswith=texto))
        correlativo=tamaño+1
        if correlativo < 10:
            correlativo="00"+str(correlativo)
        elif correlativo < 100:
            correlativo = "0"+str(correlativo)
        #Codigo de Usuario al estilo -- mv17012 ---
        codigo=texto+year+correlativo
        #----- No se como hacer si se registra alguien con tilde en el primer apellido ----
        #----- Pero es poco probable que ocurra :P -----------------------

        #Crear usuario
        usuario=self.model(
            codigoUsuario=codigo,
            email=self.normalize_email(email),
            primerNombre=primerNombre,
            segundoNombre=segundoNombre,
            primerApellido=primerApellido,
            segundoApellido=segundoApellido,
            password=password
        )

        usuario.set_password(password)
        usuario.save()
        return usuario
    
    def create_superuser(self, primerNombre,segundoNombre,primerApellido, segundoApellido,email, password = None):
        usuario=self.create_user(
            email=self.normalize_email(email),
            primerNombre=primerNombre,
            segundoNombre=segundoNombre,
            primerApellido=primerApellido,
            segundoApellido=segundoApellido,
            password=password
        )
        usuario.es_activo=True
        usuario.es_staff = True
        usuario.es_superuser=True
        usuario.save()
        return usuario


class Usuario(AbstractBaseUser, PermissionsMixin):
    codigoUsuario = models.CharField(primary_key=True,max_length=7,unique=True)
    primerNombre = models.CharField(db_column='PRIMER_NOMBRE', max_length=30, null=True)
    segundoNombre=models.CharField(db_column='SEGUNDO_NOMBRE', max_length=30, null=True)
    primerApellido = models.CharField(db_column='PRIMER_APELLIDO', max_length=30, null=True)
    segundoApellido = models.CharField(db_column='SEGUNDO_APELLIDO', max_length=30, null=True)
    sexo = models.CharField(db_column='SEXO', max_length=1, default='-')
    direccion=models.CharField(db_column='DIRECCION', max_length=120, null=True)
    email = models.EmailField(db_column='EMAIL', max_length=100, blank=True, null=True, unique=True)
    es_activo = models.BooleanField(db_column='ES_ACTIVO', default=True)
    es_staff = models.BooleanField(db_column='ES_STAFF', default=False)
    es_superuser = models.BooleanField(db_column='IS_SUPERUSER', default=False)
    last_login = models.DateField(db_column='LAST_LOGIN', null=True)
    fechaCreacion = models.DateTimeField(db_column='FECHA_CREACION', default=timezone.now)
    fechaNacimiento = models.DateField(db_column='FECHA_NACMIENTO', null=True)
    objects = UsuarioManager()

    USERNAME_FIELD="email"
    NAME_FIELD = "primerNombre"
    REQUIRED_FIELDS = ['primerNombre', 'segundoNombre', 'primerApellido','segundoApellido']

    def __str__(self):
        return f'{self.email}'
    
    def has_perm(self,perm,obj = None):
        return True
    
    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.es_staff  
    @property
    def is_active(self):
        return self.es_activo
    @property
    def is_superuser(self):
        return self.es_superuser