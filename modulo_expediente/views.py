from time import time
from django.shortcuts import render
from django.db.models import Q
from modulo_expediente.serializers import PacienteSerializer, ContieneConsultaSerializer
from django.core import serializers
from datetime import datetime
from modulo_expediente.filters import PacienteFilter
from modulo_expediente.models import Consulta, Paciente, ContieneConsulta, Expediente, SignosVitales
from modulo_control.models import Enfermera, Empleado
from modulo_expediente.forms import DatosDelPaciente
from django.http import JsonResponse
import json
from datetime import date
ROL=4
ROL_DOCTOR=1
ROL_ENFERMERA=2
ROL_LIC_LABORATORIO=3
ROL_SECRETARIA=4
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

    return render(request,"expediente/sala.html",{'rol':ROL,'ROL_DOCTOR':ROL_DOCTOR,
                                                    'ROL_ENFERMERA':ROL_ENFERMERA,
                                                    'ROL_LIC_LABORATORIO':ROL_LIC_LABORATORIO,
                                                    'ROL_SECRETARIA':ROL_SECRETARIA})

#Metodo que devuelve los datos del paciente en json
def get_paciente(request, id_paciente):
    paciente=Paciente.objects.filter(id_paciente=id_paciente)
    serializer=PacienteSerializer(paciente, many= True)
    return JsonResponse(serializer.data, safe=False)

#Metodo que devuelve los datos del objeto contiene consulta en json
def agregar_cola(request, id_paciente):
    expediente=Expediente.objects.get(id_paciente_id=id_paciente)
    idExpediente=expediente.id_expediente
    fecha=datetime.now()
    try:
        contieneconsulta=ContieneConsulta.objects.get(expediente_id=idExpediente, fecha_de_cola__year=fecha.year, 
                                                       fecha_de_cola__month=fecha.month, 
                                                       fecha_de_cola__day=fecha.day)
        response={
            'type':'warning',
            'title':'Error',
            'data':'El Paciente ya existe en la cola'
        }
        return JsonResponse(response, safe=False)
    except ContieneConsulta.DoesNotExist:
        try:
            numero=ContieneConsulta.objects.filter(fecha_de_cola__year=fecha.year, 
                            fecha_de_cola__month=fecha.month, 
                            fecha_de_cola__day=fecha.day).last().numero_cola +1
        except:
            numero=1
        #Los siguientes objetos tendrán datos unicamente para prueba
        #Creando objeto enfermera
        enfermera=Enfermera()
        enfermera.empleado_id='am22001'
        enfermera.save()
        #Creando objetos signos vitales
        signosvitales=SignosVitales()
        signosvitales.unidad_temperatura='F'
        signosvitales.unidad_peso='Lbs'
        signosvitales.unidad_presion_arterial_diastolica=''
        signosvitales.unidad_presion_arterial_sistolica=''
        signosvitales.unidad_frecuencia_cardiaca=''
        signosvitales.unidad_saturacion_oxigeno=''
        signosvitales.valor_temperatura=1
        signosvitales.valor_peso=45.00
        signosvitales.valor_presion_arterial_diastolica=1
        signosvitales.valor_presion_arterial_sistolica=1
        signosvitales.valor_frecuencia_cardiaca=1
        signosvitales.valor_saturacion_oxigeno=1
        signosvitales.enfermera_id=enfermera.id_enfermera
        signosvitales.save()
        #Creando objeto Consulta
        consulta=Consulta()
        consulta.signos_vitales_id=signosvitales.id_signos_vitales
        consulta.save()
        #Creando Objeto contieneCola
        contieneconsulta=ContieneConsulta()
        contieneconsulta.expediente=expediente
        contieneconsulta.numero_cola=numero
        contieneconsulta.consumo_medico=0
        contieneconsulta.estado_cola_medica='1'
        contieneconsulta.fase_cola_medica='2'
        contieneconsulta.consulta_id=consulta.id_consulta
        contieneconsulta.save()
        response={
            'type':'success',
            'title':'Exito',
            'data':'Paciente agregado a la cola'
        }
        return JsonResponse(response, safe=False)

#Metodo que devuelve una lista de constieneConsulta filtrado por la fecha de hoy
def  get_contieneConsulta(request):
    fecha=datetime.now()
    contieneconsulta=ContieneConsulta.objects.filter(fecha_de_cola__year=fecha.year, 
                    fecha_de_cola__month=fecha.month, 
                    fecha_de_cola__day=fecha.day)
    serializer=ContieneConsultaSerializer(contieneconsulta, many=True)
    return JsonResponse(serializer.data, safe=False)


def  get_cola(request):
    fecha=datetime.today()
    lista=[]
    if(ROL==ROL_SECRETARIA):
        contiene_consulta=ContieneConsulta.objects.filter(fecha_de_cola__year=fecha.year, 
                        fecha_de_cola__month=fecha.month, 
                        fecha_de_cola__day=fecha.day).select_related('expediente__id_paciente')
        
        for fila in contiene_consulta:
                diccionario={
                    "numero_cola":"",
                    "nombre":"",
                    "apellidos":"",
                    "fase_cola_medica":"",
                    "consumo_medico":"",
                    "estado_cola_medica":"",
                }
                
                diccionario["numero_cola"]= fila.numero_cola
                diccionario["nombre"]=fila.expediente.id_paciente.nombre_paciente
                diccionario["apellidos"]=fila.expediente.id_paciente.apellido_paciente
                diccionario["fase_cola_medica"]= fila.get_fase_cola_medica_display()
                diccionario["consumo_medico"]= fila.consumo_medico
                diccionario["estado_cola_medica"]= fila.get_estado_cola_medica_display()
                
    elif (ROL==ROL_ENFERMERA):
        contiene_consulta=ContieneConsulta.objects.filter(fecha_de_cola__year=fecha.year, 
                        fecha_de_cola__month=fecha.month, 
                        fecha_de_cola__day=fecha.day).select_related('expediente__id_paciente')
        
        
        for fila in contiene_consulta:
                diccionario={
                    "numero_cola":"",
                    "nombre":"",
                    "apellidos":"",
                }
                
                diccionario["numero_cola"]= fila.numero_cola
                diccionario["nombre"]=fila.expediente.id_paciente.nombre_paciente
                diccionario["apellidos"]=fila.expediente.id_paciente.apellido_paciente
    lista.append(diccionario)
    del diccionario

    return JsonResponse( lista, safe=False)

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

#vista de datosdelpaciente ayala
def crear_expediente(request):
    formulario = DatosDelPaciente(request.GET)
    print(formulario.is_valid)
   # if request.method == "POST": 
    if formulario.is_valid():
        formulario.save()
            
    return render(request,"datosdelPaciente.html",{'formulario':formulario})
