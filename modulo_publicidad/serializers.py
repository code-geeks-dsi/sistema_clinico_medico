from rest_framework import serializers

from modulo_publicidad.models import Publicacion, ImagenPublicacion

class ImagenPublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenPublicacion
        fields = (
            'id_imagen',
            'archivo'
            )
        depth=1

class PublicacionSerializer(serializers.ModelSerializer):
    imagenes=ImagenPublicacionSerializer(many = True)
    class Meta:
        model = Publicacion
        fields = (
            'id_publicacion', 
            'servicio', 
            'descripcion', 
            'fecha_creacion', 
            'fecha_ultima_edicion', 
            'validez_fecha_inicio', 
            'validez_fecha_fin', 
            'cantidad_visitas', 
            'imagenes'
            )
        depth=1
