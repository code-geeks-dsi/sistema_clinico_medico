from cProfile import label
from tkinter import Widget
from django import forms
from modulo_publicidad.models import *
class PublicacionForm(forms.ModelForm):
        class Meta:
                model=Publicacion
                exclude=('fecha_creacion','cantidad_visitas','id_publicacion')
                widgets={
                        'descripcion': forms.Textarea(attrs={
                                                  'class': 'form-control', 
                                                  "rows":5,
                                                  "cols":20,
                                }),
                }
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for field in self.fields:
                        self.fields[field].widget.attrs.update({'class': 'form-control'})

class PublicacionImagenForm(forms.ModelForm):
        class Meta:
                model=Imagen
                exclude=('publicacion','id_imagen')
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for field in self.fields:
                        self.fields[field].widget.attrs.update({'class': 'form-control'})

class DescuentoForm(forms.ModelForm):
        class Meta:
                model=Descuento

                exclude=('servicio','id_descuento')
                widgets = {
                        'fecha_expedicion': forms.DateInput(
                                format=('%Y-%m-%d'),
                                attrs={
                                        'placeholder':'Fecha de Creación',
                                        'label':'Fecha de Creación',
                                        'type': 'date',
                                }),
                        'fecha_expiracion': forms.DateInput(
                                format=('%Y-%m-%d'),
                                attrs={
                                        'placeholder':'Fecha de Vencimiento',
                                        'label':'Fecha de Vencimiento',
                                        'type': 'date'
                                }),
                        
                }
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for field in self.fields:
                        self.fields[field].widget.attrs.update({'class': 'form-control','required': False})