from django import forms
from modulo_publicidad.models import *

class PublicidadForm(forms.ModelForm):
        class Meta:
                model=Publicacion
                exclude=('fecha_creacion','cantidad_visitas','id_publicacion')

class PublicidadImagenForm(forms.ModelForm):
        class Meta:
                model=Imagen
                exclude=('fecha_creacion','cantidad_visitas','id_imagen')