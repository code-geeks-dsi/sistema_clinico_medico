from django import forms
from django.forms import ModelForm, TextInput
from django import forms
from .models import Consulta, Paciente, Medicamento

class DateInput(forms.DateInput):
    input_type = 'datetime-local'

class DatosDelPaciente(ModelForm):
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
            'nombre_paciente': TextInput(
               attrs={'class': 'form-control', 
               'placeholder': 'Ingrese los nombres',
              } 
            ),
            'apellido_paciente': TextInput(
               attrs={'class': 'form-control', 
               'placeholder': 'Ingrese los apellidos',
              } 
            ),
            'direccion_paciente': TextInput(
               attrs={'class': 'form-control', 
               'placeholder': 'Calle, número de casa, Ciudad, Departamento',
              } 
            ),
            'email_paciente': TextInput(
               attrs={'class': 'form-control', 
               'placeholder': 'example@gmail.com',
              } 
            ),
            'responsable': TextInput(
               attrs={'class': 'form-control', 
               'placeholder': 'Nombres Apellidos',
              } 
            ),

}

class IngresoMedicamentos(ModelForm):
    class Meta:
        model = Medicamento
        fields = ('nombre_comercial', 'nombre_generico','cantidad_medicamento','unidad_medicamento')

class ConsultaFormulario(ModelForm):
  # diagnostico=forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
  # sintoma=forms.CharField(widget=forms.Textarea(attrs={"resize": "vertical",
  #   'min-width': '-webkit-fill-available'}))
  class Meta:
    model=Consulta
    fields=['diagnostico','sintoma']
    widgets = {
            'diagnostico': forms.Textarea(attrs={
                                                  "rows":5,
                                                  "cols":20
                                                  }),
            'sintoma': forms.Textarea(attrs={
                                                  "rows":5,
                                                  "cols":20
                                                  })

              }
