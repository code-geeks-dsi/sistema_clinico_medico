from pyexpat import model
from rest_framework import serializers
from .models import CategoriaExamen, ExamenLaboratorio

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
