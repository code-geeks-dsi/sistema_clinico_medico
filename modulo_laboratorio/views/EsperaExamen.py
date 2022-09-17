import datetime
from datetime import datetime
from django.http import JsonResponse
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

""" @login_required(login_url='/login/')   
def bitacora_templete(request):
    if request.user.roles.codigo_rol=='ROL_LIC_LABORATORIO':
        return render(request,"laboratorio/bitacora.html")
    else:
        return render(request,"Control/error403.html") """

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
        examenes_en_proceso=Count(
                'examen_laboratorio', 
                filter=Q(fase_examenes_lab=Resultado.OPCIONES_FASE[1][0])|
                Q(fase_examenes_lab=Resultado.OPCIONES_FASE[2][0])
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
    
