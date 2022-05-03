from django.shortcuts import render

# Create your views here.

def busqueda_paciente(request):
    f = PacienteFilter(request.GET, queryset=Paciente.objects.all())
    return render(request, 'busquedaPaciente.html', {'filter': f})


def vista_sala_espera(request):
    return render(request,"salaEspera.html")

