import django_filters
from modulo_expediente.models import Paciente

class PacienteFilter(django_filters.FilterSet):
    class Meta:
        model = Paciente
        fields = ['nombre_paciente',
        'apellido_paciente',
        'fecha_nacimiento_paciente',
        'sexo_paciente',
        'direccion_paciente',
        'email_paciente',
        'responsable',]