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

def get_paciente (request , id_paciente):
        paciente=list(Paciente.objects.values())
        lista =[]
        for i in range(len(paciente)):
            if paciente[i]["id_paciente"] == id_paciente:
                diccionario={
                    "id_paciente":"",
                    "nombre_paciente":"",
                    "apellido_paciente":"",
                    "fecha_nacimiento_paciente":"",
                    "sexo_paciente":"",
                    "direccion_paciente":"",
                    "email_paciente":"",
                    "responsable":""
                }
                diccionario["id_paciente"]= paciente[i]["id_paciente"]
                diccionario["nombre_paciente"]= paciente[i]["nombre_paciente"]
                diccionario["apellido_paciente"]= paciente[i]["apellido_paciente"]
                diccionario["fecha_nacimiento_paciente"]= paciente[i]["fecha_nacimiento_paciente"]
                diccionario["sexo_paciente"]= paciente[i]["sexo_paciente"]
                diccionario["direccion_paciente"]= paciente[i]["direccion_paciente"]
                diccionario["email_paciente"]= paciente[i]["email_paciente"]
                diccionario["responsable"]= paciente[i]["responsable"]
                lista.append(diccionario);
                del diccionario
        return JsonResponse(lista, safe=False)

