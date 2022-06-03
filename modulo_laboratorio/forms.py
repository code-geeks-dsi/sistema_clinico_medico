from cgitb import enable
from dataclasses import fields
from django import forms

from modulo_laboratorio.models import ContieneValor, Parametro

class ContieneValorForm(forms.ModelForm):
        dato=forms.DecimalField(max_digits=12, decimal_places=3,initial=0)
        nombre_parametro = forms.CharField(required=False)
        unidad_parametro = forms.CharField(required=False)
        id_parametro=forms.IntegerField(required=False)
        class Meta:
                model=ContieneValor
                fields=('dato','nombre_parametro','unidad_parametro','id_parametro')