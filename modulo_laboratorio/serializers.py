from email.policy import default
from pyexpat import model
from rest_framework import serializers
from .models import CategoriaExamen, ExamenLaboratorio, Resultado
from datetime import datetime
from dateutil.relativedelta import relativedelta
class CategoriaExamenSerializer(serializers.ModelSerializer):
    nombre_examen = serializers.CharField(source='examen_laboratorio.nombre_examen')
    id_examen = serializers.IntegerField(source='examen_laboratorio.id_examen_laboratorio')
    class Meta:
        model = CategoriaExamen
        fields=['id_examen', 'nombre_examen']

class Examenserializer(serializers.ModelSerializer):
    muestra=serializers.CharField(source='get_tipo_muestra_display')
    class Meta:
        model=ExamenLaboratorio
        fields=['muestra', 'nombre_examen']

class ResultadoSerializer(serializers.ModelSerializer):
    nombre_examen=serializers.CharField(source='examen_laboratorio.nombre_examen')
    numero_orden=serializers.CharField(source='orden_de_laboratorio.numero_cola_orden')
    class Meta:
        model=Resultado
        fields=['id_resultado', 'nombre_examen','numero_orden','numero_cola_resultado','fase_examenes_lab']

class ResultadoLaboratorioSerializer(serializers.ModelSerializer):
    nombre=serializers.CharField(source='orden_de_laboratorio.expediente.id_paciente.nombre_paciente')
    apellidos=serializers.CharField(source='orden_de_laboratorio.expediente.id_paciente.apellido_paciente')
    edad=serializers.SerializerMethodField()
    sexo=serializers.CharField(source='orden_de_laboratorio.expediente.id_paciente.sexo_paciente')
    nombre_examen=serializers.CharField(source='examen_laboratorio.nombre_examen')
    numero_orden=serializers.CharField(source='orden_de_laboratorio.numero_cola_orden')
    fase_examen_lab=serializers.CharField(source='get_fase_examenes_lab_display')
    
    fecha=serializers.DateTimeField(format="%d/%b/%Y  %I:%M %p",source='fecha_hora_toma_de_muestra')
    id_expediente=serializers.CharField(source='orden_de_laboratorio.expediente.id_expediente')
    url_resultado=serializers.CharField(default="url resultado")

    def get_edad(self,obj):
        return relativedelta(datetime.now(), obj.orden_de_laboratorio.expediente.id_paciente.fecha_nacimiento_paciente).years
    
    class Meta:
        model=Resultado
        fields=['numero_orden','numero_cola_resultado','nombre','apellidos','sexo','edad', 'nombre_examen','fase_examen_lab','fecha','id_resultado','id_expediente','url_resultado']
