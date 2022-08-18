from modulo_expediente.serializers import ContieneConsultaSerializer
from datetime import datetime
from modulo_expediente.models import (
    Consulta,  ContieneConsulta, Expediente, 
    RecetaMedica, SignosVitales)
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@login_required()
#Metodo que devuelve los datos del objeto contiene consulta en json
def agregar_cola(request, id_paciente):
    expediente=Expediente.objects.get(id_paciente_id=id_paciente)
    fecha=datetime.now()
    try:
        contieneconsulta=ContieneConsulta.objects.get(expediente_id=expediente, fecha_de_cola__year=fecha.year, fecha_de_cola__month=fecha.month, fecha_de_cola__day=fecha.day)
        response={
            'type':'warning',
            'title':'Error',
            'data':'El Paciente ya existe en la cola'
        }
        return JsonResponse(response, safe=False)
    except:
        try:
            numero=ContieneConsulta.objects.filter(fecha_de_cola__year=fecha.year, 
                            fecha_de_cola__month=fecha.month, 
                            fecha_de_cola__day=fecha.day).last().numero_cola +1
        except:
            numero=1
        
        #Creando Objeto contieneCola
        contieneconsulta=ContieneConsulta()
        contieneconsulta.expediente=expediente
        contieneconsulta.numero_cola=numero
        receta=RecetaMedica()
        #Creando objeto Consulta comprobando si es seguimiento o nueva consulta
        try:
            ultima_consulta=ContieneConsulta.objects.filter(expediente=expediente).select_related('consulta').latest('fecha_de_cola') 
            dar_seguimiento=ultima_consulta.consulta.dar_seguimiento
        except ContieneConsulta.DoesNotExist:
            dar_seguimiento=False
        if(dar_seguimiento==True):
            contieneconsulta.consulta_id=ultima_consulta.consulta.id_consulta
            consulta=ultima_consulta.consulta
        else:
            consulta=Consulta()
            consulta.save()
            contieneconsulta.consulta_id=consulta.id_consulta
        contieneconsulta.save()
        receta.consulta=consulta
        SignosVitales.objects.create(consulta=consulta)
        receta.save()
        
        
        response={
            'type':'success',
            'title':'Exito',
            'data':'Paciente agregado a la cola'
        }
        return JsonResponse(response, safe=False)

@login_required()
def  get_cola(request):
    fecha=datetime.now()
    lista=[]
    rol=request.user.roles.codigo_rol

    if(rol=='ROL_DOCTOR'):
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
            
            filterData['fase_cola_medica']=ContieneConsulta.OPCIONES_FASE[2][0]
            filterData['fecha_de_cola__year']=fecha.year 
            filterData['fecha_de_cola__month']=fecha.month
            filterData['fecha_de_cola__day']=fecha.day

        contiene_consulta=ContieneConsulta.objects.filter(**filterData).select_related('expediente__id_paciente')
        
        for fila in contiene_consulta:
            diccionario={
                "id_consulta":"",
                "numero_cola":"",
                "nombre":"",
                "apellidos":"",
                "fase_cola_medica":"",
                "fecha_de_cola":""
            }
            #En id_consulta devuelve el id_de los signos
            diccionario['id_consulta']=fila.consulta.id_consulta
            diccionario["numero_cola"]= fila.numero_cola
            diccionario["nombre"]=fila.expediente.id_paciente.nombre_paciente
            diccionario["apellidos"]=fila.expediente.id_paciente.apellido_paciente
            diccionario["fase_cola_medica"]= fila.get_fase_cola_medica_display()
            diccionario["fecha_de_cola"]= fila.fecha_de_cola.strftime("%d/%b/%Y")
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