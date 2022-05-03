from django.shortcuts import render

# Create your views here.
def busqueda_paciente(request):
    f = PacienteFilter(request.GET, queryset=Paciente.objects.all())
    return render(request, 'busquedaPaciente.html', {'filter': f})