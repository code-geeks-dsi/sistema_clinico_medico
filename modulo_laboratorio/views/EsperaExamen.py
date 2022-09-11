
from django.urls import reverse
import datetime
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from modulo_control.models import Rol
from modulo_laboratorio.models import Categoria, CategoriaExamen, EsperaExamen
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.views import View

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
    if request.user.roles.codigo_rol=='ROL_LIC_LABORATORIO' or request.user.roles.codigo_rol=='ROL_SECRETARIA':
        categorias= Categoria.objects.all()
        data={}
        try:

            rutina=CategoriaExamen.objects.filter(categoria=categorias[0].id_categoria)
            data["Categoria"]=categorias 
            data["Examen"]=rutina
        except IndexError:
            data["Categoria"]=[]
            data["Examen"]=[]

        roles=Rol.objects.values_list('codigo_rol','id_rol').all()
        data['rol']=request.user.roles.id_rol
        for rol in roles:
            data[rol[0]]=rol[1]
        return render(request,"laboratorio/salaLaboratorio.html",data)
    else:
        return render(request,"Control/error403.html")

# REHACER
# def agregar_examen_cola(request):
#     id_paciente=request.POST.get('id_paciente',0)
#     id_examen_laboratorio=request.POST.get('id_examen_laboratorio',0)
#     fecha_hoy=datetime.now()
#     examen_item=EsperaExamen.objects.filter(expediente__id_paciente__id_paciente=id_paciente,fecha__year=fecha_hoy.year, 
#                         fecha__month=fecha_hoy.month, 
#                         fecha__day=fecha_hoy.day).first()
#     if examen_item is None:
#         examen_item=EsperaExamen.create(id_paciente,id_examen_laboratorio)
#         examen_item.save()
#         response={
#                 'type':'success',
#                 'title':'Guardado!',
#                 'data':'Examen agregado a la cola'
#             }
#     else:
#         response={
#                 'type':'warning',
#                 'data':'El examen ya existe en la cola!'
#             }
#     return JsonResponse(response, safe=False)
class agregar_orden_de_examenes(View):

    def post(self, request, *args, **kwargs): 
        id_paciente=int(self.kwargs['id_paciente'])
        print("paciente ".id_paciente)
        pass
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

# cambiar fase orden de examen
def cambiar_fase_secretaria(request):
    id_resultado=request.POST.get('id_resultado',0)
    id_expediente=request.POST.get('id_expediente',0)
    item=EsperaExamen.objects.get(resultado__id_resultado=id_resultado,expediente__id_expediente=id_expediente)
    item.fase_examenes_lab=EsperaExamen.OPCIONES_FASE[1][0]
    item.resultado.fecha_hora_toma_de_muestra=now
   
    item.save()
    response={
            'type':'success',
            'title':'Muestras entregadas!',
            'data':'Examen en proceso'
        }

    return JsonResponse(response, safe=False)

# cambiar fase resultado de examen de laboratorio
# cambiar la fase de un examen en cola a resultados listos
def cambiar_fase_laboratorio(request):
    id_resultado=request.POST.get('id_resultado',0)
    id_expediente=request.POST.get('id_expediente',0)
    item=EsperaExamen.objects.get(resultado__id_resultado=id_resultado,expediente__id_expediente=id_expediente)
    item.fase_examenes_lab=EsperaExamen.OPCIONES_FASE[2][0]
    item.resultado.fecha_hora_elaboracion_de_reporte=now
    item.save()
    response={
            'type':'success',
            'data':'Resultados Listos'
        }

    return JsonResponse(response, safe=False)