from cProfile import label
from xml.etree.ElementInclude import include
from django import forms
from modulo_expediente.models import TipoConsulta
from modulo_publicidad.models import *
class PublicacionForm(forms.ModelForm):
        class Meta:
                model=Publicacion
                exclude=('fecha_creacion','cantidad_visitas','id_publicacion','servicio')
                widgets={
                        'descripcion': forms.Textarea(attrs={
                                                  'class': 'form-control', 
                                                  "rows":5,
                                                  "cols":20,
                        }),
                        'validez_fecha_fin': forms.DateInput(
                        format=('%Y-%m-%d'),
                        attrs={
                                'placeholder':'Fecha de Inicio',
                                'label':'Fecha de Creación',
                                'type': 'date',
                        }),
                        'validez_fecha_inicio': forms.DateInput(
                        format=('%Y-%m-%d'),
                        attrs={
                                'placeholder':'Fecha de Fin',
                                'label':'Fecha de Creación',
                                'type': 'date',
                        }),
                }
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for field in self.fields:
                        self.fields[field].widget.attrs.update({'class': 'form-control'})

class PublicacionImagenForm(forms.ModelForm):
        class Meta:
                model=ImagenPublicacion
                exclude=('publicacion','id_imagen')
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for field in self.fields:
                        self.fields[field].widget.attrs.update({'class': 'form-control'})
class ServicioImagenForm(forms.ModelForm):
        class Meta:
                model=ImagenServicio
                exclude=('servicio','id_imagen')
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for field in self.fields:
                        self.fields[field].widget.attrs.update({'class': 'form-control'})

class DescuentoForm(forms.ModelForm):
        class Meta:
                model=Descuento

                exclude=('servicio','id_descuento')
                widgets = {
                        'validez_fecha_fin': forms.DateInput(
                        format=('%Y-%m-%d'),
                        attrs={
                                'placeholder':'Fecha de Inicio',
                                'label':'Fecha de Creación',
                                'type': 'date',
                        }),
                        'validez_fecha_inicio': forms.DateInput(
                        format=('%Y-%m-%d'),
                        attrs={
                                'placeholder':'Fecha de Fin',
                                'label':'Fecha de Creación',
                                'type': 'date',
                        }),
                        
                }
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for field in self.fields:
                        self.fields[field].widget.attrs.update({'class': 'form-control','required': False})
#Servicios Médicos
class ServicioMedicoForm(forms.ModelForm):
        area= forms.ModelChoiceField(queryset=TipoConsulta.objects.all(), required=False)
        crear_tipo_consulta=forms.BooleanField(label='Otro:',initial=False,required=False)
        otro= forms.CharField(label="",required=False)
        class Meta:
                model=Servicio
                fields=('nombre','precio','descripcion')
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['otro'].widget.attrs.update({'class': 'disabled','required': False})