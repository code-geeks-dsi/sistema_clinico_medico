
import django_filters
from modulo_expediente.models import Medicamento, Paciente

class PacienteFilter(django_filters.FilterSet):
    apellido_paciente = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Paciente
        exclude=['sexo_paciente','direccion_paciente','responsable','fecha_nacimiento_paciente','email_paciente','nombre_paciente']
class MedicamentoFilter(django_filters.FilterSet):
    nombre_generico = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Medicamento
        exclude=['nombre_comercial', 'nombre_generico','cantidad_medicamento','unidad_medicamento']