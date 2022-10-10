from email.policy import default
from django.db import models

class Servicio(models.Model):
    id_servicio=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.nombre
    # class Meta:
    #     abstract=True

# Implementaciones de Servicio
class ServicioMedico(Servicio):
    id_servicio_medico=models.AutoField(primary_key=True)
    servicio=models.ForeignKey('Servicio', on_delete=models.CASCADE, null=False,related_name='servicios_medicos')
    tipo_consulta=models.ForeignKey('modulo_expediente.TipoConsulta', on_delete=models.CASCADE, null=False)

class ServicioLaboratorioClinico(Servicio):
    id_servicio_laboratorio_clinico=models.AutoField(primary_key=True)
    servicio=models.ForeignKey('Servicio', on_delete=models.CASCADE, null=False,related_name='servicios_laboratorio_clinico')
    examen_laboratorio=models.ForeignKey('modulo_laboratorio.ExamenLaboratorio', on_delete=models.CASCADE, null=False)

class Descuento(models.Model):
    id_descuento=models.AutoField(primary_key=True)
    servicio=models.ForeignKey("Servicio", on_delete=models.CASCADE,related_name='descuentos')
    codigo_descuento=models.CharField(max_length=15)
    fecha_expedicion=models.DateField(auto_now_add=True, null=False)
    fecha_expiracion=models.DateField(null=True)
    cantidad_descuento=models.DecimalField(max_digits=10,decimal_places=2)
    restricciones=models.TextField()

class Publicacion(models.Model):
    id_publicidad=models.AutoField(primary_key=True)
    servicio=models.ForeignKey("Servicio", on_delete=models.CASCADE,related_name='publicaciones')
    descripcion=models.TextField()
    fecha_creacion=models.DateField(auto_now_add=True)
    cantidad_visitas=models.IntegerField(default=0)

class Imagen(models.Model):
    id_imagen=models.AutoField(primary_key=True)
    publicidad=models.ForeignKey('Publicacion', on_delete=models.CASCADE,related_name='imagenes')
    descripcion=models.CharField(max_length=25)



