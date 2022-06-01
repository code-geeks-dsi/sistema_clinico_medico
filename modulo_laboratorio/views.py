
from django.urls import reverse
import datetime

from curses import pair_content
import json
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from modulo_control.models import Rol
from modulo_expediente.models import Paciente
from modulo_laboratorio.models import Categoria, CategoriaExamen, EsperaExamen, ExamenLaboratorio, Resultado
from modulo_laboratorio.serializers import CategoriaExamenSerializer
from dateutil.relativedelta import relativedelta
# Create your views here.

# Templete Sala de Espera laboratorio
def sala_laboratorio(request):
    categorias= Categoria.objects.all()
    rutina=CategoriaExamen.objects.filter(categoria=1)
    roles=Rol.objects.values_list('codigo_rol','id_rol').all()
    data={}
    data["Categoria"]=categorias 
    data["Examen"]=rutina
    data['rol']=request.user.roles.id_rol
    for rol in roles:
        data[rol[0]]=rol[1]
    return render(request,"laboratorio/salaLaboratorio.html",data)

#View Recuperar Examenes por categoria
def get_categoria_examen(request, id_categoria):
    response={
            'data':'El Paciente ya existe en la cola',
            'accion':2
        }
    id_cat=id_categoria
    categoriaExamen=CategoriaExamen.objects.filter(categoria=id_cat)
    serializer = CategoriaExamenSerializer(categoriaExamen, many= True)
    response['data']=serializer.data
    return JsonResponse(response, safe=False)

def agregar_examen_cola(request):
    id_paciente=request.POST.get('id_paciente',0)
    id_examen_laboratorio=request.POST.get('id_examen_laboratorio',0)
    examen_item=EsperaExamen.create(id_paciente,id_examen_laboratorio)
    examen_item.save()
    response={
            'type':'success',
            'title':'Guardado!',
            'data':'Examen agregado a la cola'
        }

    return JsonResponse(response, safe=False)


    return JsonResponse(response, safe=False)
#View que retorna lista de examenes en espera
def get_cola_examenes(request):
    fecha_hoy=datetime.now()
    lista=[]
    espera_examen=EsperaExamen.objects.filter(fecha__year=fecha_hoy.year, 
                        fecha__month=fecha_hoy.month, 
                        fecha__day=fecha_hoy.day,fase_examenes_lab=EsperaExamen.OPCIONES_FASE[0][0]).select_related('expediente__id_paciente')
    for fila in espera_examen:
        diccionario={
            "numero_cola_laboratorio":"",
            "nombre":"",
            "apellidos":"",
            "examen":"",
            "fase_examenes_lab":"",
            "fecha":"",
            "consumo_laboratorio":"",
            "estado_pago_laboratorio":"",
            "url_resultado":"",
        }
        diccionario["numero_cola_laboratorio"]= fila.numero_cola_laboratorio
        diccionario["nombre"]=fila.expediente.id_paciente.nombre_paciente
        diccionario["apellidos"]=fila.expediente.id_paciente.apellido_paciente
        diccionario["examen"]=fila.resultado.examen_laboratorio.nombre_examen
        diccionario["fase_examenes_lab"]= fila.get_fase_examenes_lab_display()
        diccionario["fecha"]=fila.fecha
        diccionario["consumo_laboratorio"]= fila.consumo_laboratorio
        diccionario["estado_pago_laboratorio"]= fila.get_estado_pago_laboratorio_display()
        #  en caso de ser secretaria la url debe de cambiarse a cambiar fase
        diccionario["url_resultado"]= reverse('elaborar_resultado',kwargs={'id_resultado':fila.resultado.id_resultado})
        lista.append(diccionario)
        del diccionario
    return JsonResponse( {'data':lista}, safe=False)

def elaborar_resultados_examen(request,id_resultado):
        examen=ExamenLaboratorio.objects.get(resultado=id_resultado)
        return HttpResponse("Elaborar examen de laboratorio "+examen.nombre_examen+"!")

