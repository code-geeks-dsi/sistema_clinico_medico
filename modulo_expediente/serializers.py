from rest_framework import serializers
from modulo_expediente.models import Medicamento, Paciente, ContieneConsulta
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
        fields = fields=['presentacion']
class ContieneConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContieneConsulta
        fields = '__all__'
