from django.shortcuts import render
from modulo_expediente.filters import PacienteFilter
from modulo_expediente.models import Paciente

# Create your views here.

def busqueda_paciente(request):
    filter = PacienteFilter(request.GET, queryset=Paciente.objects.all())
    return render(request, 'busquedaPaciente.html', {'filter': filter})


def vista_sala_espera(request):
    return render(request,"salaEspera.html")

