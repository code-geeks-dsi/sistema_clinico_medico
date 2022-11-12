from email.policy import default
from enum import unique
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
""""
Por simplificación considerar el servicio y servicio médico como uno solo,
mismo caso aplica para servicio y servicio laboratorio clínico.

Relacionar el servicio al detalle de transacción y agregar atributo 
booleano estado_de_pago a Orden Examen (EsperaExamen) y
Cola Consulta (ContieneConsulta)
"""

class Servicio(models.Model):
    id_servicio=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio=models.DecimalField(max_digits=10,decimal_places=2)
    descripcion=models.TextField()
    cantidad_visitas=models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

# Implementaciones de Servicio
class ServicioMedico(models.Model):
    id_servicio_medico=models.AutoField(primary_key=True)
    servicio=models.OneToOneField('Servicio', on_delete=models.CASCADE, null=False,related_name='servicios_medicos')
    tipo_consulta=models.ForeignKey('modulo_expediente.TipoConsulta',on_delete=models.CASCADE, null=False)
    def __str__(self):
        return str(self.tipo_consulta.nombre)+" $ "+str(self.servicio.precio)+str(self.servicio.descripcion)+str(self.servicio.id_servicio)
class ServicioLaboratorioClinico(models.Model):
    id_servicio_laboratorio_clinico=models.AutoField(primary_key=True)
    servicio=models.OneToOneField('Servicio', on_delete=models.CASCADE, null=False,related_name='servicios_laboratorio_clinico')
    examen_laboratorio=models.OneToOneField('modulo_laboratorio.ExamenLaboratorio', on_delete=models.CASCADE, null=False)
    def __str__(self):
        return str(self.examen_laboratorio.nombre_examen)+" $ "+str(self.servicio.precio)+str(self.servicio.descripcion)+str(self.servicio.id_servicio)

# Descuentos asociados a cada Servicio
class Descuento(models.Model):
    id_descuento=models.AutoField(primary_key=True)
    publicacion=models.OneToOneField("Publicacion", on_delete=models.CASCADE,related_name='descuentos')
    codigo_descuento=models.CharField(max_length=15,unique=True)
    validez_fecha_inicio=models.DateField(null=True)
    validez_fecha_fin=models.DateField(null=True)
    cantidad_descuento=models.DecimalField(max_digits=10,decimal_places=2)
    porcentaje_descuento=models.IntegerField()
    restricciones=models.TextField()
    fecha_creacion=models.DateField(auto_now_add=True)
    fecha_ultima_edicion=models.DateField(auto_now=True)

# Modelos de Publicación
class Publicacion(models.Model):
    id_publicacion=models.AutoField(primary_key=True)
    servicio=models.ForeignKey("Servicio", on_delete=models.CASCADE,related_name='publicaciones')
    descripcion=models.TextField()
    fecha_creacion=models.DateField(auto_now_add=True)
    fecha_ultima_edicion=models.DateField(auto_now=True)
    validez_fecha_inicio=models.DateField(null=True)
    validez_fecha_fin=models.DateField(null=True)
    cantidad_visitas=models.IntegerField(default=0)

# Isaí 
class ImagenPublicacion(models.Model):
    id_imagen=models.AutoField(primary_key=True)
    publicacion=models.ForeignKey('Publicacion', on_delete=models.CASCADE,related_name='imagenes')
    archivo=models.ImageField(null=True, blank=True, storage=S3Boto3Storage(
                            bucket_name='code-geek-medic',
                            default_acl='public-read',
                            location='static',
                            ),upload_to='publicaciones')

class ImagenServicio(models.Model):
    id_imagen=models.AutoField(primary_key=True)
    servicio=models.ForeignKey('Servicio', on_delete=models.CASCADE,related_name='imagenes')
    archivo=models.ImageField(null=True, blank=True, storage=S3Boto3Storage(
                            bucket_name='code-geek-medic',
                            default_acl='public-read',
                            location='static',
                            ),upload_to='servicios')

class Visita(models.Model):
    id_visita=models.CharField(primary_key=True, max_length=20)
    cantidad_visitas=models.IntegerField(default=0)