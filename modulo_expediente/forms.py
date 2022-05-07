from django import forms
from .models import Post

class DatosDelPaciente(forms.form):
    nombre_paciente = forms.CharField()
    apellido_paciente = forms.CharField()
    fecha_nacimiento_paciente = forms.DateField()
    sexo_paciente = forms.CharField()
    direccion_paciente = forms.CharField()
    email_paciente = forms.EmailField()
    responsable = forms.CharField()

     class Meta:
        model = Post
        fields = ('nombre_paciente', 'apellido_paciente','fecha_nacimiento_paciente','sexo_paciente','direccion_paciente','email_paciente','responsable')
        

