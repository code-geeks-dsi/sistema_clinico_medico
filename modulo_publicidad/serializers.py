from rest_framework import serializers

from modulo_publicidad.models import Publicacion

class PublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacion
        fields = '__all__'
        depth=1
