from rest_framework import serializers

from modulo_publicidad.models import *

class ImagenPublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenPublicacion
        fields = (
            'id_imagen',
            'archivo'
            )
        depth=1

class ImagenServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenServicio
        fields = '__all__'
        depth=1

class DescuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descuento
        fields = '__all__'
        depth=1


class PublicacionSerializer(serializers.ModelSerializer):
    descuentos=DescuentoSerializer()
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
            'imagenes',
            'descuentos'
            )
        depth=1


class ServicioSerializer(serializers.ModelSerializer):
    imagenes=ImagenServicioSerializer(many = True)
    publicaciones=PublicacionSerializer(many=True)
    class Meta:
        model = Servicio
        fields = '__all__'
        depth=1

class ServicioMedicoSerializer(serializers.ModelSerializer):
    servicio=ServicioSerializer()
    class Meta:
        model = ServicioMedico
        fields = '__all__'
        depth=1

class ServicioMedicoSerializerCorto(serializers.ModelSerializer):
    class Meta:
        model = ServicioMedico
        fields = '__all__'
        depth=1