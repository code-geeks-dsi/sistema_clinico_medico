import django_filters

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Paciente
        fields = ['__all__']