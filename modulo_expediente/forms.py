
from dataclasses import fields
from django import forms
from django.forms import ModelForm, NumberInput, TextInput, Select
from django import forms
from .models import Consulta, Dosis, Paciente, Medicamento, ReferenciaMedica

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
            'sexo_paciente': Select(
               attrs={'class': 'form-control'
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
        widgets = {
            'nombre_comercial': TextInput(
               attrs={'class': 'form-control', 
               'placeholder': 'Ingrese el nombre comercial del medicamento',
              } 
            ),
            'nombre_generico': TextInput(
               attrs={'class': 'form-control', 
               'placeholder': 'Ingrese el nombre generico del medicamento',
              } 
            ),
            'cantidad_medicamento': NumberInput(
               attrs={'class': 'form-control'
              } 
            ),
            'unidad_medicamento': Select(
               attrs={'class': 'form-select'
              } 
            ),
        }
class ConsultaFormulario(ModelForm):
  
  class Meta:
    model=Consulta
    fields=['consulta_por','presente_enfermedad','examen_fisico','diagnostico']
    widgets = {
            'consulta_por': forms.Textarea(attrs={
                                                  "rows":5,
                                                  "cols":20
                                                  }),
            'presente_enfermedad': forms.Textarea(attrs={
                                                  "rows":5,
                                                  "cols":20
                                                  }),
            'examen_fisico': forms.Textarea(attrs={
                                                  "rows":5,
                                                  "cols":20
                                                  }),
            'diagnostico': forms.Textarea(attrs={
                                                  "rows":5,
                                                  "cols":20
                                                  }),
              }
class DosisFormulario(ModelForm):
  medicamento= forms.ModelChoiceField(queryset=Medicamento.objects.all())
  medicamento.widget.attrs.update({'class': 'form-select'})
  class Meta:
    model=Dosis
    fields='__all__'
  def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['frecuencia_dosis'].widget.attrs.update({'class': 'form-control'})
        self.fields['unidad_frecuencia_dosis'].widget.attrs.update({'class': 'form-select'})
        self.fields['cantidad_dosis'].widget.attrs.update({'class': 'form-control'})
        self.fields['unidad_de_medida_dosis'].widget.attrs.update({'class': 'form-select'})
        self.fields['periodo_dosis'].widget.attrs.update({'class': 'form-control'})
        self.fields['unidad_periodo_dosis'].widget.attrs.update({'class': 'form-select'})

class ReferenciaMedicaForm(ModelForm):
    class Meta:
      model=ReferenciaMedica
      fields='__all__'
      exclude=['consulta']