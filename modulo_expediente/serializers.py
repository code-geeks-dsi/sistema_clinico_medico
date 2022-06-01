from rest_framework import serializers
from modulo_expediente.models import Dosis, Medicamento, Paciente, ContieneConsulta
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
        fields = '__all__'
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
    medicamentos = serializers.CharField(source='medicamento')
    presentacion=serializers.CharField(source='medicamento.presentacion')
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
        fields = ['medicamentos','cantidad', 'presentacion','frecuencia', 'periodo']