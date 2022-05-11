from django import forms
from django.forms import ModelForm
from django import forms
from .models import Paciente

class DateInput(forms.DateInput):
    input_type = 'datetime-local'

class DatosDelPaciente(ModelForm):
    
    '''nombre_paciente = forms.CharField()
    apellido_paciente = forms.CharField()
    fecha_nacimiento_paciente = forms.DateField()
    sexo_paciente = forms.CharField()
    direccion_paciente = forms.CharField()
    email_paciente = forms.EmailField()
    responsable = forms.CharField()'''
    #fecha_nacimiento_paciente = forms.DateField()
    class Meta:
        model = Paciente
        fields = ('nombre_paciente', 'apellido_paciente','sexo_paciente','direccion_paciente','email_paciente','responsable','fecha_nacimiento_paciente')
        widgets = {
            'fecha_nacimiento_paciente': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
               'placeholder': 'Select a date',
               'type': 'date'
              }),
}
