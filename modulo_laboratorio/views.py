
import datetime

from curses import pair_content
import json
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from modulo_expediente.models import Paciente
from modulo_laboratorio.models import Categoria, CategoriaExamen, EsperaExamen, Resultado
from modulo_laboratorio.serializers import CategoriaExamenSerializer
from dateutil.relativedelta import relativedelta
# Create your views here.

# Templete Sala de Espera laboratorio
def sala_laboratorio(request):
    categorias= Categoria.objects.all()
    rutina=CategoriaExamen.objects.filter(categoria=1)
    return render(request,"laboratorio/salaLaboratorio.html", {"Categoria":categorias, "Examen":rutina})

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

    return JsonResponse({}, safe=False)


    return JsonResponse(response, safe=False)
#View que retorna lista de examenes en espera
def get_cola_examenes(request):
    fecha=datetime.now()
    lista=[]
    espera_examen=EsperaExamen.objects.filter(fecha__year=fecha.year, 
                        fecha__month=fecha.month, 
                        fecha__day=fecha.day).select_related('expediente__id_paciente')

    if EsperaExamen.fase_examenes_lab==1:
        for fila in espera_examen:
                diccionario={
                    "numero_cola_laboratorio":"",
                    "nombre":"",
                    "apellidos":"",
                    "sexo":"",
                    "fase_examenes_lab":"",
                    "consumo_laboratorio":"",
                    "estado_pago_laboratorio":"",
                }
                diccionario["numero_cola_laboratorio"]= fila.numero_cola
                diccionario["nombre"]=fila.expediente.id_paciente.nombre_paciente
                diccionario["apellidos"]=fila.expediente.id_paciente.apellido_paciente
                diccionario["sexo"]=fila.expediente.id_paciente.sexo_paciente
                diccionario["fase_examenes_lab"]= fila.get_fase_examenes_lab_display()
                diccionario["consumo_laboratorio"]= fila.consumo_laboratorio
                diccionario["estado_pago_laboratorio"]= fila.get_estado_pago_laboratorio_display()
                lista.append(diccionario)
    return JsonResponse( lista, safe=False)
