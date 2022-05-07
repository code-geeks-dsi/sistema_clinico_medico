
from django.shortcuts import render
from modulo_expediente.filters import PacienteFilter
from modulo_expediente.forms import DatosDelPaciente, FormularioVenta
from modulo_expediente.models import Paciente
from django.http import JsonResponse
# Create your views here.

def busqueda_paciente(request):
    
    filter = PacienteFilter(request.GET, queryset=Paciente.objects.all())
    apellidosList=Paciente.objects.values("apellido_paciente").all()
    # queryset=Paciente.objects.filter(nombre_paciente=request.GET.get('nombre_paciente',""),apellido_paciente=request.GET.get('apellido_paciente',""))
    return render(request, 'busquedaPaciente.html', {'filter': filter,'apellidosList':apellidosList})


def vista_sala_espera(request):
    return render(request,"salaEspera.html")

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
#vista de datosdelpaciente ayala
def crear_expediente(request):
    formulario = DatosDelPaciente(request.GET)
    formulario2 = FormularioVenta(request.GET)
    print(formulario.is_valid)
   # if request.method == "POST": 
    if formulario.is_valid():
        formulario.save()
            
    return render(request,"datosdelPaciente.html",{'formulario':formulario,"creaventa":formulario2})

from time import time
from django.shortcuts import render
from modulo_expediente.serializers import PacienteSerializer, ContieneConsultaSerializer
from django.core import serializers
from datetime import datetime
from modulo_expediente.filters import PacienteFilter
from modulo_expediente.models import Consulta, Paciente, ContieneConsulta, Expediente
from django.http import JsonResponse
import json
from datetime import date
# Create your views here.

def busqueda_paciente(request):
    result= PacienteFilter(request.GET, queryset=Paciente.objects.all())
    pacientes =PacienteSerializer(result.qs, many=True)
    return JsonResponse({'data':pacientes.data})
     #la clave tiene que ser data para que funcione con el metodo. 

def autocompletado_apellidos(request):
    
    apellidos=Paciente.objects.values("apellido_paciente").all()
    apellidosList=[]
    for apellido in apellidos:
        apellidosList.append(apellido['apellido_paciente'])
    return JsonResponse({"data":apellidosList})
    #la clave tiene que ser data para que funcione con el metodo. 

def sala_consulta(request):
    return render(request,"expediente/sala.html")

#Metodo que devuelve los datos del paciente en json
def get_paciente(request, id_paciente):
    paciente=Paciente.objects.filter(id_paciente=id_paciente)
    serializer=PacienteSerializer(paciente, many= True)
    return JsonResponse(serializer.data, safe=False)

#Metodo que devuelve los datos del objeto contiene consulta en json
def agregar_cola(request, id_paciente):
    expediente=Expediente.objects.get(id_paciente_id=id_paciente)
    codExpediente=expediente.id_expediente
    fecha=datetime.now()
    try:
        numero=ContieneConsulta.objects.filter(fecha_de_cola__year=fecha.year, 
                         fecha_de_cola__month=fecha.month, 
                         fecha_de_cola__day=fecha.day).last().numero_cola +1
    except:
        numero=1
    #Creando Objeto contieneCola
    try:
        contieneconsulta=ContieneConsulta()
        contieneconsulta.expediente=expediente
        contieneconsulta.numero_cola=numero
        contieneconsulta.consumo_medico=0
        contieneconsulta.estado_cola_medica='1'
        contieneconsulta.fase_cola_medica='2'
        contieneconsulta.save()
        response={
            'type':'success',
            'title':'Exito',
            'data':'Paciente agregado a la cola'
        }
    except:
        response={
            'type':'warning',
            'title':'Error',
            'data':'Paciente ya existe en la cola'
        }
    
    return JsonResponse(response, safe=False)

#Metodo que devuelve una lista de constieneConsulta filtrado por la fecha de hoy
def  get_contieneConsulta(request):
    fecha=datetime.now()
    '''
    contiene_consulta=list(ContieneConsulta.objects.values())
    lista=[]
    for i in range(len(contiene_consulta)):
        if contiene_consulta[i]["fecha_de_cola"] == fecha_actual:
            diccionario={
                "id":"",
                "numero_cola":"",
                "fecha_de_cola":"",
                "consumo_medico":"",
                "estado_cola_medica":"",
                "fase_cola_medica":"",
                "consulta_id":"",
                "expediente_id":""
            }
            diccionario["id"]= contiene_consulta[i]["id"]
            diccionario["numero_cola"]= contiene_consulta[i]["numero_cola"]
            diccionario["fecha_de_cola"]= contiene_consulta[i]["fecha_de_cola"]
            diccionario["consumo_medico"]= contiene_consulta[i]["consumo_medico"]
            diccionario["estado_cola_medica"]= contiene_consulta[i]["estado_cola_medica"]
            diccionario["fase_cola_medica"]= contiene_consulta[i]["fase_cola_medica"]
            diccionario["consulta_id"]= contiene_consulta[i]["consulta_id"]
            diccionario["expediente_id"]= contiene_consulta[i]["expediente_id"]
            lista.append(diccionario)
            del diccionario
            '''
    contieneconsulta=ContieneConsulta.objects.filter(fecha_de_cola__year=fecha.year, 
                    fecha_de_cola__month=fecha.month, 
                    fecha_de_cola__day=fecha.day)
    serializer=ContieneConsultaSerializer(contieneconsulta, many=True)
    return JsonResponse(serializer.data, safe=False)

#Método que elimina una persona de la cola
def eliminar_cola(request, id_paciente):
    fecha=datetime.now()
    expediente=Expediente.objects.get(id_paciente=id_paciente)
    idExpediente=expediente.id_expediente
    try:
        contieneconsulta=ContieneConsulta.objects.filter(expediente_id=idExpediente, fecha_de_cola__year=fecha.year, 
                         fecha_de_cola__month=fecha.month, 
                         fecha_de_cola__day=fecha.day)
        contieneconsulta.delete()
        response={
            'type':'sucess',
            'title':'Eliminado',
            'data':'Paciente eliminado de la cola.'
        }
    except:
        response={
            'type':'warning',
            'title':'Error',
            'data':'El paciente no se encuentra en la cola'
        }
    return JsonResponse(response, safe=False)

