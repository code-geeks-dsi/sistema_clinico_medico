from django.shortcuts import render
from modulo_expediente.serializers import PacienteSerializer
from django.core import serializers
from modulo_expediente.filters import PacienteFilter
from modulo_expediente.models import Paciente
from django.http import JsonResponse
import json

# Create your views here.

def busqueda_paciente(request):
    result= PacienteFilter(request.GET, queryset=Paciente.objects.all())
    pacientes =PacienteSerializer(result.qs, many=True)
    return JsonResponse({'pacientes':pacientes.data})

def autocompletado_apellidos(request):
    
    apellidos=Paciente.objects.values("apellido_paciente").all()
    apellidosList=[]
    for apellido in apellidos:
        apellidosList.append(apellido['apellido_paciente'])
    return JsonResponse({"apellidos":apellidosList})


def sala_consulta(request):
    return render(request,"busquedaPaciente.html")

