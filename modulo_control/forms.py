#from dataclasses import fields
from django.forms import ModelForm
from .models import *

class EmpleadoForm(ModelForm):
    class Meta:
        model=Empleado
        fields=['nombres','apellidos','sexo','direccion','email','fechaNacimiento','roles']

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ['especialidad_doctor','jvmp']
# class EnfermeraForm(ModelForm):
#     class Meta:
#         model = Enfermera
#         fields = '__all__'

class LicLaboratorioClinicoForm(ModelForm):
    class Meta:
        model = LicLaboratorioClinico
        fields = ['jvplc']

# class SecretariaForm(ModelForm):
#     class Meta:
#         model = Secretaria
#         fields = '__all__'
