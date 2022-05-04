from django.shortcuts import render
from modulo_expediente.filters import PacienteFilter
from modulo_expediente.models import Paciente

# Create your views here.

def busqueda_paciente(request):
    
    filter = PacienteFilter(request.GET, queryset=Paciente.objects.all())
    apellidosList=Paciente.objects.values("apellido_paciente").all()
    # queryset=Paciente.objects.filter(nombre_paciente=request.GET.get('nombre_paciente',""),apellido_paciente=request.GET.get('apellido_paciente',""))
    return render(request, 'busquedaPaciente.html', {'filter': filter,'apellidosList':apellidosList})


def vista_sala_espera(request):
    return render(request,"salaEspera.html")

