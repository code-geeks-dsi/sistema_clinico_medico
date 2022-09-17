from django.shortcuts import render
from modulo_laboratorio.models import  (EsperaExamen, Resultado)
from django.contrib.auth.decorators import login_required
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


def verificar_fase_orden_laboratorio(orden):
    mensaje=None
    '''
    Revisando si ya se entregaron todas las muestras de todos 
    los examenes que pertenecen a la orden
    '''
    verificacion=Resultado.objects.values('orden_de_laboratorio').filter(orden_de_laboratorio=orden).annotate(
        examenes_en_recepcion=Count(
                'examen_laboratorio', 
                filter=Q(fase_examenes_lab=Resultado.OPCIONES_FASE[0][0])
            ),
        examenes_en_proceso=Count(
                'examen_laboratorio', 
                filter=Q(fase_examenes_lab=Resultado.OPCIONES_FASE[1][0])
            ),
        examenes_listos=Count(
                'examen_laboratorio', 
                filter=Q(fase_examenes_lab=Resultado.OPCIONES_FASE[2][0])
            ),
        examenes_entregados=Count(
                'examen_laboratorio', 
                filter=Q(fase_examenes_lab=Resultado.OPCIONES_FASE[3][0])
            ),
        total=Count('examen_laboratorio')
        )
    total_examenes=verificacion[0]['total']
    examenes_en_recepcion=verificacion[0]['examenes_en_recepcion']
    examenes_en_proceso=verificacion[0]['examenes_en_proceso']
    examenes_listos=verificacion[0]['examenes_listos']
    examenes_entregados=verificacion[0]['examenes_entregados']

    # En el caso de que ya se entregaron todas las muestras entonces
    # se cambia la fase de la orden (EsperaExamen)
    if (examenes_en_recepcion>0 and
        orden.fase_examenes_lab!=EsperaExamen.OPCIONES_FASE_ORDEN[0][0]):
        orden.fase_examenes_lab=EsperaExamen.OPCIONES_FASE_ORDEN[0][0]
        mensaje={
                'type':'info',
                'title':'Recepción de Muestras',
                'data':'Orden En Recepción de Muestras Médicas'
                }
    elif (examenes_en_recepcion==0 and 
        examenes_en_proceso>0 and
        orden.fase_examenes_lab!=EsperaExamen.OPCIONES_FASE_ORDEN[1][0]):
        orden.fase_examenes_lab=EsperaExamen.OPCIONES_FASE_ORDEN[1][0]
        mensaje={
                'type':'info',
                'title':'En Proceso',
                'data':'Orden Completa En Proceso.'
                }
    elif (examenes_en_recepcion==0 and 
        examenes_en_proceso==0 and
        examenes_listos>0 and
        orden.fase_examenes_lab!=EsperaExamen.OPCIONES_FASE_ORDEN[2][0]):
        orden.fase_examenes_lab=EsperaExamen.OPCIONES_FASE_ORDEN[2][0]
        mensaje={
                'type':'info',
                'title':'Lista',
                'data':'Orden Completa Lista.'
                }
    elif (examenes_en_recepcion==0 and 
        examenes_en_proceso==0 and
        examenes_listos==0 and
        examenes_entregados>0 and
        orden.fase_examenes_lab!=EsperaExamen.OPCIONES_FASE_ORDEN[3][0]):
        orden.fase_examenes_lab=EsperaExamen.OPCIONES_FASE_ORDEN[3][0]
        mensaje={
                'type':'info',
                'title':'Entregada',
                'data':'Orden Completa Entregada.'
                }
    orden.save()
    return mensaje
    
