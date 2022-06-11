
from unittest import result
from urllib import response
from wsgiref.util import request_uri
from django.urls import reverse
import datetime
from django.forms import formset_factory
from curses import pair_content
import json
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from modulo_control.models import Empleado, LicLaboratorioClinico, Rol
from modulo_expediente.models import Expediente, Paciente
from modulo_expediente.serializers import PacienteSerializer
from modulo_laboratorio.forms import ContieneValorForm
from modulo_laboratorio.models import Categoria, CategoriaExamen, ContieneValor, EsperaExamen, ExamenLaboratorio, Parametro, RangoDeReferencia, Resultado
from modulo_laboratorio.serializers import CategoriaExamenSerializer
from dateutil.relativedelta import relativedelta
from django.template.loader import get_template
from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string
import tempfile
from django.utils.timezone import now
# Create your views here.

# Templete Sala de Espera laboratorio
def sala_laboratorio(request):
    if request.user.roles.codigo_rol=='ROL_LIC_LABORATORIO' or request.user.roles.codigo_rol=='ROL_SECRETARIA':
        categorias= Categoria.objects.all()
        rutina=CategoriaExamen.objects.filter(categoria=categorias[0].id_categoria)
        roles=Rol.objects.values_list('codigo_rol','id_rol').all()
        data={}
        data["Categoria"]=categorias 
        data["Examen"]=rutina
        data['rol']=request.user.roles.id_rol
        for rol in roles:
            data[rol[0]]=rol[1]
        return render(request,"laboratorio/salaLaboratorio.html",data)
    else:
        return render(request,"Control/error403.html")


#View Recuperar Examenes por categoria
def get_categoria_examen(request, id_categoria):
    response={
            'data':'El Examen ya existe en la cola',
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
    fecha_hoy=datetime.now()
    examen_item=EsperaExamen.objects.filter(expediente__id_paciente__id_paciente=id_paciente,resultado__examen_laboratorio__id_examen_laboratorio=id_examen_laboratorio,fecha__year=fecha_hoy.year, 
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

#View que retorna lista de examenes en espera
def get_cola_examenes(request):
    tipo_consulta=request.GET.get('tipo_consulta','')
    fecha_hoy=datetime.now()
    lista=[]
    if(request.user.roles.codigo_rol=='ROL_SECRETARIA'):
        espera_examen=EsperaExamen.objects.filter(fecha__year=fecha_hoy.year, 
                        fecha__month=fecha_hoy.month, 
                        fecha__day=fecha_hoy.day).select_related('expediente__id_paciente').order_by('numero_cola_laboratorio')
    elif (request.user.roles.codigo_rol=='ROL_LIC_LABORATORIO'):
        if tipo_consulta=="1":
            # espera_examen=EsperaExamen.objects.filter(fase_examenes_lab=EsperaExamen.OPCIONES_FASE[1][0]).select_related('expediente__id_paciente').order_by('numero_cola_laboratorio')                
            # espera_examen=EsperaExamen.objects.filter(fecha__year=fecha_hoy.year, 
            #             fecha__month=fecha_hoy.month, 
            #             fecha__day=fecha_hoy.day,fase_examenes_lab=EsperaExamen.OPCIONES_FASE[1][0]).select_related('expediente__id_paciente').order_by('numero_cola_laboratorio')
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

def elaborar_resultados_examen(request,id_resultado):
        data={}
        lic_laboratorio=LicLaboratorioClinico.objects.get(empleado=request.user)
        resultado=Resultado.objects.get(id_resultado=id_resultado)
        resultado.lic_laboratorio=lic_laboratorio
        resultado.save()
        # verificando si los resultados han sido entregados
        espera_examen=EsperaExamen.objects.get(resultado=resultado)
        if espera_examen.fase_examenes_lab==EsperaExamen.OPCIONES_FASE[3][0]:
            readonly=True
        examen=resultado.examen_laboratorio
        valores=ContieneValor.objects.filter(resultado=resultado)
        parametros=Parametro.objects.filter(examen_de_laboratorio=examen)
        ContieneValorFormSet=formset_factory(ContieneValorForm)
        #recuperando parametros que pertenecen a este examen
        cantidad_parametros=len(parametros)
        data['form-TOTAL_FORMS']= str(cantidad_parametros)
        data['form-INITIAL_FORMS']= str(0)
        # # asignando valores por defecto para unidad y nombre parametro
        if len(valores)==0:
            for i in range(cantidad_parametros):
                parametro=parametros[i]
                data['form-'+str(i)+'-unidad_parametro']=parametro.unidad_parametro
                data['form-'+str(i)+'-nombre_parametro']=parametro.nombre_parametro
                data['form-'+str(i)+'-dato']=0
                
        else:
            for i in range(cantidad_parametros):
                valor=valores[i]
                data['form-'+str(i)+'-unidad_parametro']=valor.parametro.unidad_parametro
                data['form-'+str(i)+'-nombre_parametro']=valor.parametro.nombre_parametro
                data['form-'+str(i)+'-dato']=valor.dato
        formset=ContieneValorFormSet(data)
        if request.method=='GET':
            paciente= EsperaExamen.objects.get(resultado=id_resultado).expediente.id_paciente
            edad = relativedelta(datetime.now(), paciente.fecha_nacimiento_paciente)
            response={
                'formset':formset,
                'nombre_examen':examen.nombre_examen,
                'paciente':paciente,
                'edad':edad,
                'cantidad_valores':len(valores)
            }
            return render(request,'laboratorio/resultados.html',response)
        elif request.method=='POST':
            
            if formset.is_valid():
                try:
                    resultado.fecha_hora_elaboracion_de_reporte=datetime.now()
                    resultado.save()
                    for i in range(cantidad_parametros):
                        dato=request.POST.get('form-'+str(i)+'-dato')
                        obj, created=ContieneValor.objects.update_or_create(parametro=parametros[i],resultado=resultado,defaults={'dato':dato})
                        
                    response={
                        'type':'success',
                        'data':'Guardado!'
                    }
                except:
                    response={
                        'type':'warning',
                        'data':"Datos no validos!"
                    }
            else:
                response={
                    'type':'warning',
                    'data':'Datos no validos!'
                }
            
            return JsonResponse(response,safe=False)
            

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

#Método para descargar examenes de laboratorio
#Método que genera los pdf 
def generar_pdf(request,id_resultado):
    data={}
    esperaExamen=EsperaExamen.objects.get(resultado_id=id_resultado)
    # actualizando la fase del resultado
    esperaExamen.fase_examenes_lab=EsperaExamen.OPCIONES_FASE[3][0]
    esperaExamen.save()
    #consultando datos del paciente
    idExpediente=esperaExamen.expediente_id
    expediente=Expediente.objects.get(id_expediente=idExpediente)
    idpaciente=expediente.id_paciente_id
    paciente=Paciente.objects.get(id_paciente=idpaciente)
    edad = relativedelta(datetime.now(), paciente.fecha_nacimiento_paciente)
    #consultando datos del examen
    resultado=Resultado.objects.get(id_resultado=id_resultado)
    idexamen=resultado.examen_laboratorio_id
    examenlab=ExamenLaboratorio.objects.get(id_examen_laboratorio=idexamen)
    fecha=resultado.fecha_hora_elaboracion_de_reporte
    #Consultando datos del encargado de emitir examen
    id_lic=resultado.lic_laboratorio_id
    licdeLab=LicLaboratorioClinico.objects.get(id_lic_laboratorio=id_lic)
    codigo_empleado=licdeLab.empleado_id
    empleado=Empleado.objects.get(codigo_empleado=codigo_empleado)
    #Consultando resultados
    contieneValor=ContieneValor.objects.filter(resultado_id=id_resultado)
    parametros=ContieneValor.objects.filter(resultado_id=id_resultado).values('parametro').distinct()
    referencias=RangoDeReferencia.objects.filter(parametro__in=parametros)
    
    data={'contieneValor':contieneValor, 'paciente':paciente,'edad':edad,'fecha':fecha,'empleado':empleado,'examenlab':examenlab,'referencias':referencias}
    #puede recibir la info como diccionario
    html_string = render_to_string('ResultadosDeLaboratorio.html',data)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="resultados.pdf"'
    response['Content-Transfer-Encoding'] = 'binary'
    #Crea un archivo temporal
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response

def inicio(request):
    if request.user.roles.codigo_rol=='ROL_LIC_LABORATORIO':
        return render(request,"laboratorio/laboratorio.html")
    else:
        return render(request,"Control/error403.html")

def examenes_pendientes(request):
    if request.user.roles.codigo_rol=='ROL_LIC_LABORATORIO':
        return render(request,"laboratorio/examenes_pendientes.html")
    else:
        return render(request,"Control/error403.html")

def bitacora_templete(request):
    if request.user.roles.codigo_rol=='ROL_LIC_LABORATORIO':
        return render(request,"laboratorio/bitacora.html")
    else:
        return render(request,"Control/error403.html")