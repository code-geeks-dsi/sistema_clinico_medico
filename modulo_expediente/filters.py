
import django_filters
from modulo_expediente.models import Medicamento, Paciente

class PacienteFilter(django_filters.FilterSet):
    # nombre_paciente = django_filters.CharFilter(lookup_expr='icontains')
    apellido_paciente = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Paciente
        exclude=['sexo_paciente','direccion_paciente','responsable','fecha_nacimiento_paciente','email_paciente','nombre_paciente']
        # fields = ['nombre_paciente',
        # 'apellido_paciente' ]
class MedicamentoFilter(django_filters.FilterSet):
    # nombre_paciente = django_filters.CharFilter(lookup_expr='icontains')
    Medicamento = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Medicamento
        exclude=['nombre_comercial', 'nombre_generico','cantidad_medicamento','unidad_medicamento']
        # fields = ['nombre_paciente',
        # 'apellido_paciente' ]