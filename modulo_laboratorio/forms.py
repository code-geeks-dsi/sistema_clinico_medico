from django import forms

from .models import ContieneValor

class ContieneValorForm(forms.ModelForm):
        dato=forms.DecimalField(max_digits=12, decimal_places=3,initial=0)
        nombre_parametro = forms.CharField(required=False,label=None)
        unidad_parametro = forms.CharField(required=False,label=None)
        class Meta:
                model=ContieneValor
                fields=('dato','nombre_parametro','unidad_parametro',)
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['dato'].widget.attrs.update({'class': 'form-control'})