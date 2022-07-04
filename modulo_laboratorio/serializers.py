from rest_framework import serializers
from .models import CategoriaExamen

class CategoriaExamenSerializer(serializers.ModelSerializer):
    nombre_examen = serializers.CharField(source='examen_laboratorio.nombre_examen')
    id_examen = serializers.IntegerField(source='examen_laboratorio.id_examen_laboratorio')
    class Meta:
        model = CategoriaExamen
        fields = fields=['id_examen', 'nombre_examen']
