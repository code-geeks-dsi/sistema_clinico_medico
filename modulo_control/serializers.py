from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from modulo_control.models import Empleado, Rol
# class PacienteSerializer(serializers.Serializer):
#     id_paciente=serializers.IntegerField()
#     nombre_paciente = serializers.CharField(max_length=200)
#     apellido_paciente = serializers.CharField(max_length=200)
#     fecha_nacimiento_paciente = serializers.DateTimeField()
#     sexo_paciente = serializers.CharField(max_length=1)
#     direccion_paciente=serializers.CharField(max_length=200)
#     email_paciente = serializers.EmailField()
#     responsable=serializers.CharField(max_length=200)

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    nombre_rol = serializers.CharField(source='roles')
    class Meta:
        model = Empleado
        field = fields=['codigo_empleado','nombres', 'apellidos', 'nombre_rol']
##No regresa los datos de inicio de sesion como email o contraseña
class SimpleEmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        field = fields=['codigo_empleado','nombres', 'apellidos', 'direccion', 'fechaNacimiento', 'sexo','roles', 'es_activo']


