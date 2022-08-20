
from dataclasses import fields
from pyexpat import model
from django import forms
from django.forms import ModelForm, NumberInput, TextInput, Select
from django import forms
from .models import (
  Consulta, Dosis, Paciente, Medicamento, ReferenciaMedica,EvolucionConsulta,ControlSubsecuente,
  ConstanciaMedica, DocumentoExpediente, Expediente, SignosVitales, CitaConsulta

)
from django.utils.translation import gettext as _
from django.core.exceptions import NON_FIELD_ERRORS

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
    fields=['consulta_por','presente_enfermedad','examen_fisico','diagnostico','plan_tratamiento','dar_seguimiento']
    widgets = {
            'consulta_por': forms.Textarea(attrs={
                                                  'class': 'form-control', 
                                                  "rows":5,
                                                  "cols":20
                                                  }),
            'presente_enfermedad': forms.Textarea(attrs={
                                                  'class': 'form-control',               
                                                  "rows":5,
                                                  "cols":20
                                                  }),
            'examen_fisico': forms.Textarea(attrs={
                                                  'class': 'form-control',  
                                                  "rows":5,
                                                  "cols":20
                                                  }),
            'diagnostico': forms.Textarea(attrs={
                                                  'class': 'form-control',  
                                                  "rows":5,
                                                  "cols":20
                                                  }),
            'plan_tratamiento': forms.Textarea(attrs={
                                                  'class': 'form-control',  
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
      widgets={
        'consulta_por': forms.Textarea(attrs={
                                        'class': 'form-control',  
                                        "rows":3,
                                        "cols":20
                                        }
        ),
        'hospital': Select(
            attrs={'class': 'form-select'
          } 
        ),
        'especialidad': TextInput(
               attrs={'class': 'form-control', 
               'placeholder': 'Ingrese la espacialidad.',
              }
        ),
        'fecha_referencia': TextInput(
               attrs={'class': 'form-control', 
               'placeholder': 'Ingrese el nombre generico del medicamento',
               'aria-disabled':"true",
              }
        ),
        'fecha_referencia': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
               'placeholder': 'Select a date',
               'type': 'date'
              }),

      }

class ConstanciaMedicaForm(ModelForm):
    class Meta:
      model=ConstanciaMedica
      fields='__all__'
      exclude=['consulta']
      widgets={
        'diagnostico_constancia': forms.Textarea(attrs={
                                        'class': 'form-control',  
                                        "rows":3,
                                        "cols":20,
                                        'placeholder':'Ingrese el diagnostico de la consulta.'
                                        }
        ),
        'dias_reposo': NumberInput(
               attrs={'class': 'form-control', 
               'placeholder': 'Ingrese los días de reposo.',
               'min':0
              }
        ),
        'acompanante': TextInput(
                attrs={'class': 'form-control', 
               'placeholder': 'Ingrese el nombre del acompañante.',
              }
        ),
        'fecha_de_emision': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
               'placeholder': 'Select a date',
               'type': 'date'
              }),
      }
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['acompanante'].label="Acompañante"
      self.fields['dias_reposo'].label="Días de reposo"
      self.fields['diagnostico_constancia'].label="Diagnóstico"
      
class HojaEvolucionForm(ModelForm):
    class Meta:
      model=EvolucionConsulta
      fields=['observacion']
      widgets={
        'observacion': forms.Textarea(attrs={
                                        'class': 'form-control',  
                                        "rows":3,
                                        "cols":20
                                        }
        )}


class ControlSubsecuenteform(ModelForm):
  class Meta:
    model=ControlSubsecuente
    fields=['observacion']
    widgets={
        'observacion': forms.Textarea(attrs={
                                        'class': 'form-control',  
                                        "rows":1,
                                        "cols":80
                                        }
        ),
        'fecha': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
               'placeholder': 'Select a date',
               'type': 'date'
              }),
        }


class DocumentoExpedienteForm(ModelForm):
  class Meta:
    model=DocumentoExpediente
    fields='__all__'
    exclude=['empleado']

    
class antecedentesForm(ModelForm):
  class Meta:
    model=Expediente
    fields=['antecedentes_personales', 'antecedentes_familiares']
    widgets={
        'antecedentes_familiares': forms.Textarea(attrs={
                                        'class': 'form-control',  
                                        "rows":3,
                                        "cols":20
                                        }
        ),
        'antecedentes_personales': forms.Textarea(attrs={
                                        'class': 'form-control',  
                                        "rows":3,
                                        "cols":20
                                        }
        )}


class SignosVitalesForm(ModelForm):
  def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
          self.fields[field].widget.attrs.update({'class': 'form-control col'})
        
        self.fields['valor_presion_arterial_diastolica'].widget.attrs.update({'regex':'\d{0,3}'})
        self.fields['valor_presion_arterial_sistolica'].widget.attrs.update({'regex':'\d{0,3}'})
        self.fields['unidad_presion_arterial_diastolica'].widget.attrs.update({'readonly':'readonly'})
        self.fields['unidad_presion_arterial_sistolica'].widget.attrs.update({'readonly':'readonly'})
        self.fields['unidad_frecuencia_cardiaca'].widget.attrs.update({'readonly':'readonly'})
        self.fields['unidad_saturacion_oxigeno'].widget.attrs.update({'readonly':'readonly'})
  class Meta:
    model=SignosVitales
    fields=('valor_temperatura',
            'unidad_temperatura',
            'valor_peso',
            'unidad_peso',
            'valor_presion_arterial_diastolica',
            'unidad_presion_arterial_diastolica',
            'valor_presion_arterial_sistolica',
            'unidad_presion_arterial_sistolica',
            'valor_frecuencia_cardiaca',
            'unidad_frecuencia_cardiaca',
            'valor_saturacion_oxigeno',
            'unidad_saturacion_oxigeno',
            )
    labels = {
            'valor_temperatura': 'Temperatura',
            'valor_presion_arterial_diastolica':'Presión Arterial Diastólica',
            'valor_presion_arterial_sistolica':'Presión Arterial Sistólica',
            'valor_frecuencia_cardiaca':'Frecuencia Cardíaca',
            'valor_saturacion_oxigeno':'Saturación de Oxígeno',
            'valor_peso':'Peso'
        }
    
class CitaConsultaForm(ModelForm):
  class Meta:
    model=CitaConsulta
    fields='__all__'
    exclude=['empleado']
    widgets={
      'expediente': Select(
            attrs={'class': 'form-select'
          } 
        ),
      'prioridad_paciente': Select(
            attrs={'class': 'form-select'
          } 
        ),
      'observacion': TextInput(
                attrs={'class': 'form-control', 
               'placeholder': 'Ingrese una observación.',
              }
        ),
      'fecha_cita': forms.DateInput(
        format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
               'placeholder': 'Select a date',
               'type': 'date'
              }),
      'horario': Select(
            attrs={'class': 'form-select'
          } 
        ),
    }
    error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': _("Ya existe una cita programada para la fecha y hora seleccionadas."),
            }
        }

class CitaConsultaSecretariaForm(ModelForm):
  class Meta:
    model=CitaConsulta
    fields='__all__'
    widgets={
      'empleado': Select(
            attrs={'class': 'form-select'
          } 
        ),
      'expediente': Select(
            attrs={'class': 'form-select'
          } 
        ),
      'prioridad_paciente': Select(
            attrs={'class': 'form-select'
          } 
        ),
      'observacion': TextInput(
                attrs={'class': 'form-control', 
               'placeholder': 'Ingrese una observación.',
              }
        ),
      'fecha_cita': forms.DateInput(
        format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
               'placeholder': 'Select a date',
               'type': 'date'
              }),
      'horario': Select(
            attrs={'class': 'form-select'
          } 
        ),
        }
    error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': _("Ya existe una cita programada para la fecha y hora seleccionadas."),
            }
        }


