from time import time
from django.shortcuts import redirect, render
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
from django.urls import reverse
from urllib.parse import urlencode
from urllib.request import urlopen
from django.contrib.auth.decorators import login_required
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
    return render(request,"expediente/sala.html",{'rol':request.user.roles.id_rol,'ROL_DOCTOR':ROL_DOCTOR,
                                                    'ROL_ENFERMERA':ROL_ENFERMERA,
                                                    'ROL_LIC_LABORATORIO':ROL_LIC_LABORATORIO,
                                                    'ROL_SECRETARIA':ROL_SECRETARIA})

#Metodo que devuelve los datos del paciente en json
@login_required
def get_paciente(request, id_paciente):
    paciente=Paciente.objects.filter(id_paciente=id_paciente)
    serializer=PacienteSerializer(paciente, many= True)
    return JsonResponse(serializer.data, safe=False)
@login_required()
#Metodo que devuelve los datos del objeto contiene consulta en json
def agregar_cola(request, id_paciente):
    #CODIGO_EMPLEADO=1
    expediente=Expediente.objects.get(id_paciente_id=id_paciente)
    idExpediente=expediente.id_expediente
    fecha=datetime.now()
    try:
        contieneconsulta=ContieneConsulta.objects.get(expediente_id=idExpediente, fecha_de_cola__year=fecha.year, fecha_de_cola__month=fecha.month, fecha_de_cola__day=fecha.day)
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
        
        #Creando objetos signos vitales
        signosvitales=SignosVitales()
        #signosvitales.enfermera=Enfermera.objects.get(id_enfermera=CODIGO_EMPLEADO)
        signosvitales.save()
        #Creando objeto Consulta
        consulta=Consulta()
        consulta.signos_vitales_id=signosvitales.id_signos_vitales
        consulta.save()
        #Creando Objeto contieneCola
        contieneconsulta=ContieneConsulta()
        contieneconsulta.expediente=expediente
        contieneconsulta.numero_cola=numero
        contieneconsulta.consulta_id=consulta.id_consulta
        contieneconsulta.save()
        response={
            'type':'success',
            'title':'Exito',
            'data':'Paciente agregado a la cola'
        }
        return JsonResponse(response, safe=False)

#Metodo que devuelve una lista de constieneConsulta filtrado por la fecha de hoy
def  get_contiene_consulta(request):
    fecha=datetime.now()
    contieneconsulta=ContieneConsulta.objects.filter(fecha_de_cola__year=fecha.year, 
                    fecha_de_cola__month=fecha.month, 
                    fecha_de_cola__day=fecha.day)
    serializer=ContieneConsultaSerializer(contieneconsulta, many=True)
    return JsonResponse(serializer.data, safe=False)

#filtro de contiene consulta para la vista Doctor
def contiene_consulta_con_filtro(request):
    fecha=datetime.now()
    contieneconsulta=ContieneConsulta.objects.filter(fecha_de_cola__year=fecha.year, 
                    fecha_de_cola__month=fecha.month, 
                    fecha_de_cola__day=fecha.day)
    serializer=ContieneConsultaSerializer(contieneconsulta, many=True)
    return JsonResponse(serializer.data, safe=False)

@login_required()
def  get_cola(request):
    fecha=datetime.now()
    lista=[]
    rol=request.user.roles.id_rol

    if(rol==ROL_SECRETARIA):
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
            lista.append(diccionario)
    elif(rol==ROL_DOCTOR):
        #en la vista doctor se retorna el apellido de la barra de busqueda del paciente
        apellido_paciente=request.GET.get('apellido_paciente','')
        year=int(request.GET.get('year',0))
        month=int(request.GET.get('month',0))
        day=int(request.GET.get('day',0))
        isQuery=bool(request.GET.get('query',False))
        filterData={}
        if isQuery:
            filterData['expediente__id_paciente__apellido_paciente__icontains']=apellido_paciente
            # si filtra por fecha
            if year!=0 and month!=0 and day!=0:
                filterData['fecha_de_cola__year']=year 
                filterData['fecha_de_cola__month']=month
                filterData['fecha_de_cola__day']=day
            # # si se estan cargando los valores por defecto
        else:
            filterData['fecha_de_cola__year']=fecha.year 
            filterData['fecha_de_cola__month']=fecha.month
            filterData['fecha_de_cola__day']=fecha.day

        contiene_consulta=ContieneConsulta.objects.filter(**filterData).select_related('expediente__id_paciente')
        
        for fila in contiene_consulta:
            diccionario={
                "numero_cola":"",
                "nombre":"",
                "apellidos":"",
                "fase_cola_medica":"",
                "fecha_de_cola":""
            }
            
            diccionario["numero_cola"]= fila.numero_cola
            diccionario["nombre"]=fila.expediente.id_paciente.nombre_paciente
            diccionario["apellidos"]=fila.expediente.id_paciente.apellido_paciente
            diccionario["fase_cola_medica"]= fila.get_fase_cola_medica_display()
            diccionario["fecha_de_cola"]= fila.fecha_de_cola
            lista.append(diccionario)
            # del diccionario
                
    elif (rol==ROL_ENFERMERA):
        # recupera los pacientes en cola en fase anotado
        contiene_consulta=ContieneConsulta.objects.filter(fecha_de_cola__year=fecha.year, 
                        fecha_de_cola__month=fecha.month, 
                        fecha_de_cola__day=fecha.day,fase_cola_medica=ContieneConsulta.OPCIONES_FASE[1][0]).select_related('expediente__id_paciente')
        
        
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
            # del diccionario
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

#Método que crea un nuevo paciente y lo asigna a un expediente
def crear_expediente(request):
    idpaciente=request.GET.get('id', None)
    if request.method == 'GET':
        if idpaciente==None:
            formulario= DatosDelPaciente()
        else:     
            paciente=Paciente.objects.get(id_paciente=idpaciente)
            formulario = DatosDelPaciente(instance=paciente)

    else:
        if idpaciente==None:
            formulario= DatosDelPaciente(request.POST)
            if formulario.is_valid():
                new_paciente=formulario.save()
                expediente=Expediente()
                expediente.fecha_creacion_expediente=datetime.now()
                #Generando código expediente
                nombrepaciente = formulario["nombre_paciente"].value()
                apellidopaciente=formulario["apellido_paciente"].value()
                year=datetime.now().date().strftime("%Y")[2:]
                texto=nombrepaciente[0]+apellidopaciente[0]
                texto=texto.lower()#Solo texto en minusculas
                texto=texto+year
                try:
                    correlativo = correlativo = Expediente.objects.filter(codigo_expediente__startswith=texto).last().codigo_expediente
                    correlativo=int(correlativo[4:])
                except:
                    correlativo=0 
                correlativo=correlativo+1
                if correlativo < 10:
                    correlativo="00"+str(correlativo)
                elif correlativo < 100:
                    correlativo = "0"+str(correlativo)
                #Codigo de Usuario al estilo -- mv17012 ---
                codigo=texto+correlativo
                expediente.codigo_expediente=codigo
                idpaciente=list(Paciente.objects.values("id_paciente").all())
                idList=[]
                for i in idpaciente:
                    idList.append(i['id_paciente'])
                expediente.id_paciente_id=idList[-1]
                expediente.save()
                base_url = reverse('crear_expediente')
                query_string =  urlencode({'id': new_paciente.id_paciente})
                url = '{}?{}'.format(base_url, query_string)
                return redirect(url)
        else:
            paciente=Paciente.objects.get(id_paciente=idpaciente)
            formulario = DatosDelPaciente(request.POST, instance=paciente)
            formulario.save()
        
    return render(request,"datosdelPaciente.html",{'formulario':formulario})

  

def modificar_signosVitales(request, id_signos_vitales):

    signosvitales=SignosVitales.objects.get(id_signos_vitales=id_signos_vitales)
    signosvitales.unidad_temperatura=request.POST['unidad_temperatura']
    signosvitales.unidad_peso=request.POST['unidad_peso']
    signosvitales.unidad_presion_arterial_diastolica=request.POST['unidad_presion_arterial_diastolica']
    signosvitales.unidad_presion_arterial_sistolica=request.POST['unidad_presion_arterial_sistolica']
    signosvitales.unidad_frecuencia_cardiaca=request.POST['frecuencia_cardiaca']
    signosvitales.unidad_saturacion_oxigeno=request.POST['unidad_saturacion_oxigeno']
    signosvitales.valor_temperatura=request.POST['valor_temperatura']
    signosvitales.valor_peso=request.POST['valor_peso']
    signosvitales.valor_presion_arterial_diastolica=request.POST['valor_presion_arterial_diastolica']
    signosvitales.valor_presion_arterial_sistolica=request.POST['valor_presion_arterial_sistolica']
    signosvitales.valor_frecuencia_cardiaca=request.POST['valor_frecuencia_cardiaca']
    signosvitales.valor_saturacion_oxigeno=request.POST['valor_saturacion_oxigeno']
    signosvitales.save()
    response={
        'type':'success',
        'title':'Modificado',
        'data':'Se han modificado los signos vitales'
    }
    return JsonResponse(response, safe=False)
