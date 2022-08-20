from rest_framework import serializers

from modulo_expediente.models import Consulta, Dosis, Medicamento, Paciente, ContieneConsulta, SignosVitales

from modulo_expediente.models import Dosis, Medicamento, Paciente, ContieneConsulta, CitaConsulta

# class PacienteSerializer(serializers.Serializer):
#     id_paciente=serializers.IntegerField()
#     nombre_paciente = serializers.CharField(max_length=200)
#     apellido_paciente = serializers.CharField(max_length=200)
#     fecha_nacimiento_paciente = serializers.DateTimeField()
#     sexo_paciente = serializers.CharField(max_length=1)
#     direccion_paciente=serializers.CharField(max_length=200)
#     email_paciente = serializers.EmailField()
#     responsable=serializers.CharField(max_length=200)

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        exclude=('dui','pasaporte','numero_telefono')
class MedicamentoSerializer(serializers.ModelSerializer):
    presentacion = serializers.CharField(source='get_presentacion_display')
    class Meta:
        model = Medicamento
        fields = fields=['id_medicamento','nombre_generico', 'nombre_comercial', 'presentacion']
class ContieneConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContieneConsulta
        fields = '__all__'
class DosisListSerializer(serializers.ModelSerializer):
    id=serializers.CharField(source='id_dosis')
    medicamentos = serializers.CharField(source='medicamento')
    presentacion=serializers.CharField(source='medicamento.get_presentacion_display')
    cantidad = serializers.SerializerMethodField()
    frecuencia = serializers.SerializerMethodField()
    periodo = serializers.SerializerMethodField()

    def get_cantidad(self, obj):
        return '{} - {}'.format(obj.cantidad_dosis, obj.get_unidad_de_medida_dosis_display()) 
    def get_frecuencia(self, obj):
        return '{} - {}'.format(obj.frecuencia_dosis, obj.get_unidad_frecuencia_dosis_display()) 
    def get_periodo(self, obj):
        return '{} - {}'.format(obj.periodo_dosis, obj.get_unidad_periodo_dosis_display()) 
    class Meta:
        model = Dosis
        fields = ['id','medicamentos','cantidad', 'presentacion','frecuencia', 'periodo']

class DocumentoExternoSerializer(serializers.ModelSerializer):
    id_documento=serializers.IntegerField()
    titulo=serializers.CharField()
    fecha=serializers.DateTimeField(format="%d de %b de %Y a las %I:%M ")
    propietario=serializers.CharField(source='expediente.id_paciente.nombre_paciente')
    class Meta:
        model = Dosis
        fields = ['id_documento','titulo','fecha', 'propietario']

class ConsultaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = '__all__'



class CitaConsultaSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(source='id_cita_consulta')
    title=serializers.SerializerMethodField()
    start=serializers.SerializerMethodField()
    end=serializers.SerializerMethodField()
    color=serializers.SerializerMethodField()
    def get_title(self, obj):
        return '{} - Prioridad: {}'.format(obj.expediente.id_paciente.nombre_paciente, obj.get_prioridad_paciente_display()) 
    def get_start(self, obj):
        fecha= obj.fecha_cita.strftime("%Y-%m-%d")
        hora=obj.horario.hora_inicio.strftime("%H:%M")
        return f'{fecha}T{hora}'
    def get_end(self, obj):
        fecha= obj.fecha_cita.strftime("%Y-%m-%d")
        hora=obj.horario.hora_fin.strftime("%H:%M")
        return f'{fecha}T{hora}'
    def get_color(self, obj):
        if obj.prioridad_paciente == "1":#alta
            color='#e84b2c'
        elif obj.prioridad_paciente == "2":#media
            color='#e6d839'
        elif obj.prioridad_paciente == "3":#baja
            color='#7cd164'
        return color

    class Meta:
        model= CitaConsulta
        fields = ['id','title','start','end' ,'color']

