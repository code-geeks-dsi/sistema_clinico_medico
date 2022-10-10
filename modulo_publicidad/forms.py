from django import forms
from modulo_publicidad.models import *

class PublicacionForm(forms.ModelForm):
        class Meta:
                model=Publicacion
                exclude=('fecha_creacion','cantidad_visitas','id_publicacion')

class PublicacionImagenForm(forms.ModelForm):
        class Meta:
                model=Imagen
                exclude=('publicidad','id_imagen')