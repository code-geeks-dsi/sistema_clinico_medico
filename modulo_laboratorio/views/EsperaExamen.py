from django.urls import reverse
import datetime
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from modulo_control.models import Rol
from modulo_laboratorio.models import Categoria, CategoriaExamen, EsperaExamen,Resultado
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.views import View
from django.db.models import Count, Q

@login_required(login_url='/login/')   
def inicio(request):
    if request.user.roles.codigo_rol=='ROL_LIC_LABORATORIO':
        return render(request,"laboratorio/laboratorio.html")
    else:
        return render(request,"Control/error403.html")

@login_required(login_url='/login/')   
def examenes_pendientes(request):
    if request.user.roles.codigo_rol=='ROL_LIC_LABORATORIO':
        return render(request,"laboratorio/examenes_pendientes.html")
    else:
        return render(request,"Control/error403.html")

@login_required(login_url='/login/')   
def bitacora_templete(request):
    if request.user.roles.codigo_rol=='ROL_LIC_LABORATORIO':
        return render(request,"laboratorio/bitacora.html")
    else:
        return render(request,"Control/error403.html")

@login_required(login_url='/login/')  
def sala_laboratorio(request):
    if request.user.roles.codigo_rol=='ROL_SECRETARIA':
        return render(request,"laboratorio/ColaOrdenesDeExamenes.html")
    else:
        return render(request,"Control/error403.html")

# REHACER
def agregar_examen_cola(request):
    id_paciente=request.POST.get('id_paciente',0)
    id_examen_laboratorio=request.POST.get('id_examen_laboratorio',0)
    fecha_hoy=datetime.now()
    examen_item=EsperaExamen.objects.filter(expediente__id_paciente__id_paciente=id_paciente,fecha__year=fecha_hoy.year, 
                        fecha__month=fecha_hoy.month, 
                        fecha__day=fecha_hoy.day).first()
    if examen_item is None:
        examen_item=EsperaExamen.create(id_paciente,id_examen_laboratorio)
        examen_item.save()
        response={
                'type':'success',
                'title':'Guardado!',
                'data':'Examen agregado a la cola'
            }
    else:
        response={
                'type':'warning',
                'data':'El examen ya existe en la cola!'
            }
    return JsonResponse(response, safe=False)

# modificar
#View que retorna lista de examenes en espera
def get_cola_ordenes_de_examenes(request):
    tipo_consulta=request.GET.get('tipo_consulta','')
    fecha_hoy=datetime.now()
    lista=[]
    if(request.user.roles.codigo_rol=='ROL_SECRETARIA'):
        espera_examen=EsperaExamen.objects.filter(fecha__year=fecha_hoy.year, 
                        fecha__month=fecha_hoy.month, 
                        fecha__day=fecha_hoy.day).select_related('expediente__id_paciente').order_by('numero_cola_laboratorio')
        
    for fila in espera_examen:
        diccionario={
            "numero_cola_laboratorio":"",
            "nombre":"",
            "apellidos":"",
            "sexo":"",
            "edad":"",
            "examen":"",
            "fase_examenes_lab":"",
            "fecha":"",
            "consumo_laboratorio":"",
            "estado_pago_laboratorio":"",
        }
        edad=relativedelta(datetime.now(), fila.expediente.id_paciente.fecha_nacimiento_paciente).years 
        diccionario["numero_cola_laboratorio"]= fila.numero_cola_laboratorio
        diccionario["nombre"]=fila.expediente.id_paciente.nombre_paciente
        diccionario["apellidos"]=fila.expediente.id_paciente.apellido_paciente
        diccionario["sexo"]=fila.expediente.id_paciente.get_sexo_paciente_display()
        diccionario["edad"]= edad 
        diccionario["examen"]=fila.resultado.examen_laboratorio.nombre_examen
        diccionario["fase_examenes_lab"]= fila.get_fase_examenes_lab_display()
        diccionario["fecha"]=fila.fecha.strftime("%d/%b/%Y")
        diccionario["consumo_laboratorio"]= fila.consumo_laboratorio
        diccionario["estado_pago_laboratorio"]= fila.get_estado_pago_laboratorio_display()
        #  en caso de ser secretaria la url debe de cambiarse a cambiar fase
        
        diccionario["id_resultado"]= fila.resultado.id_resultado
        diccionario["id_expediente"]= fila.expediente.id_expediente
        if (request.user.roles.codigo_rol=='ROL_LIC_LABORATORIO'):
            diccionario["url_resultado"]= reverse('elaborar_resultado',kwargs={'id_resultado':fila.resultado.id_resultado})
        if (request.user.roles.codigo_rol=='ROL_SECRETARIA'):
            diccionario["url_resultado_pdf"]= reverse('generar_pdf',kwargs={'id_resultado':fila.resultado.id_resultado})
        lista.append(diccionario)
        del diccionario
    if len(lista)==0:
        response={
            'type':'warning',
            'data':'No hay examenes pendientes'
        }
    else:
        response={'data':lista}
    return JsonResponse( response , safe=False)

def get_cola_examenes_a_elaborar(request):
    tipo_consulta=request.GET.get('tipo_consulta','')
    fecha_hoy=datetime.now()
    lista=[]
    if (request.user.roles.codigo_rol=='ROL_LIC_LABORATORIO'):
        if tipo_consulta=="1":
            espera_examen=EsperaExamen.objects.filter(fase_examenes_lab=EsperaExamen.OPCIONES_FASE[1][0]).select_related('expediente__id_paciente').order_by('numero_cola_laboratorio')                
        else:
            espera_examen=EsperaExamen.objects.filter(fecha__year=fecha_hoy.year, 
                        fecha__month=fecha_hoy.month).select_related('expediente__id_paciente').order_by('numero_cola_laboratorio')
        
    for fila in espera_examen:
        diccionario={
            "numero_cola_laboratorio":"",
            "nombre":"",
            "apellidos":"",
            "sexo":"",
            "edad":"",
            "examen":"",
            "fase_examenes_lab":"",
            "fecha":"",
            "consumo_laboratorio":"",
            "estado_pago_laboratorio":"",
        }
        edad=relativedelta(datetime.now(), fila.expediente.id_paciente.fecha_nacimiento_paciente).years 
        diccionario["numero_cola_laboratorio"]= fila.numero_cola_laboratorio
        diccionario["nombre"]=fila.expediente.id_paciente.nombre_paciente
        diccionario["apellidos"]=fila.expediente.id_paciente.apellido_paciente
        diccionario["sexo"]=fila.expediente.id_paciente.get_sexo_paciente_display()
        diccionario["edad"]= edad 
        diccionario["examen"]=fila.resultado.examen_laboratorio.nombre_examen
        diccionario["fase_examenes_lab"]= fila.get_fase_examenes_lab_display()
        diccionario["fecha"]=fila.fecha.strftime("%d/%b/%Y")
        diccionario["consumo_laboratorio"]= fila.consumo_laboratorio
        diccionario["estado_pago_laboratorio"]= fila.get_estado_pago_laboratorio_display()
        #  en caso de ser secretaria la url debe de cambiarse a cambiar fase
        
        diccionario["id_resultado"]= fila.resultado.id_resultado
        diccionario["id_expediente"]= fila.expediente.id_expediente
        if (request.user.roles.codigo_rol=='ROL_LIC_LABORATORIO'):
            diccionario["url_resultado"]= reverse('elaborar_resultado',kwargs={'id_resultado':fila.resultado.id_resultado})
        if (request.user.roles.codigo_rol=='ROL_SECRETARIA'):
            diccionario["url_resultado_pdf"]= reverse('generar_pdf',kwargs={'id_resultado':fila.resultado.id_resultado})
        lista.append(diccionario)
        del diccionario
    if len(lista)==0:
        response={
            'type':'warning',
            'data':'No hay examenes pendientes'
        }
    else:
        response={'data':lista}
    return JsonResponse( response , safe=False)

def verificar_fase_orden_laboratorio(orden):
    mensaje=None
    '''
    Revisando si ya se entregaron todas las muestras de todos 
    los examenes que pertenecen a la orden
    '''
    verificacion=Resultado.objects.values('orden_de_laboratorio').filter(orden_de_laboratorio=orden).annotate(
        examenes_en_proceso=Count(
                'examen_laboratorio', 
                filter=Q(fase_examenes_lab=Resultado.OPCIONES_FASE[1][0])
            ),
        total=Count('examen_laboratorio')
        )
    total_examenes=verificacion[0]['total']
    examenes_en_proceso=verificacion[0]['examenes_en_proceso']

    # En el caso de que ya se entregaron todas las muestras entonces
    # se cambia la fase de la orden (EsperaExamen)
    if (total_examenes==examenes_en_proceso and orden.fase_examenes_lab!=EsperaExamen.OPCIONES_FASE_ORDEN[1][0]):
        orden.fase_examenes_lab=EsperaExamen.OPCIONES_FASE_ORDEN[1][0]
        mensaje={
                'type':'success',
                'title':'Orden en proceso!',
                'data':'Orden Completa En Proceso!'
                }
    elif (total_examenes>examenes_en_proceso and orden.fase_examenes_lab==EsperaExamen.OPCIONES_FASE_ORDEN[1][0]):
        orden.fase_examenes_lab=EsperaExamen.OPCIONES_FASE_ORDEN[0][0]
        mensaje={
                'type':'info',
                'title':'Recepcion de Muestras!',
                'data':'Orden En Recepcion de Muestras Medicas!'
                }
    orden.save()
    return mensaje

# cambiar fase resultado de examen de laboratorio
# cambiar la fase de un examen en cola a resultados listos
def cambiar_fase_a_listo(request):
    id_resultado=request.POST.get('id_resultado',0)
    item=Resultado.objects.get(id_resultado=id_resultado)
    item.fase_examenes_lab=Resultado.OPCIONES_FASE[2][0]
    item.fecha_hora_elaboracion_de_reporte=datetime.now()
    item.save()
    response={
            'type':'success',
            'data':'Resultados Listos'
        }

    return JsonResponse(response, safe=False)