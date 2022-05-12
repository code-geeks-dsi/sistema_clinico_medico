#from dataclasses import fields
from django.forms import ModelForm
from .models import *


class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

class EnfermeraForm(ModelForm):
    class Meta:
        model = Enfermera
        fields = '__all__'

class LicLaboratorioClinicoForm(ModelForm):
    class Meta:
        model = LicLaboratorioClinico
        fields = '__all__'

class SecretariaForm(ModelForm):
    class Meta:
        model = Secretaria
        fields = '__all__'
