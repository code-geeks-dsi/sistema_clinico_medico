
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
from modulo_control.models import Rol
from modulo_expediente.models import Expediente, Paciente
from modulo_laboratorio.forms import ContieneValorForm
from modulo_laboratorio.models import Categoria, CategoriaExamen, ContieneValor, EsperaExamen, ExamenLaboratorio, Parametro, Resultado
from modulo_laboratorio.serializers import CategoriaExamenSerializer
from dateutil.relativedelta import relativedelta
from django.template.loader import get_template
from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string
import tempfile
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


    return JsonResponse(response, safe=False)
#View que retorna lista de examenes en espera
def get_cola_examenes(request):
    fecha_hoy=datetime.now()
    lista=[]
    if(request.user.roles.codigo_rol=='ROL_SECRETARIA'):
        espera_examen=EsperaExamen.objects.filter(fecha__year=fecha_hoy.year, 
                        fecha__month=fecha_hoy.month, 
                        fecha__day=fecha_hoy.day).select_related('expediente__id_paciente').order_by('numero_cola_laboratorio')
    elif (request.user.roles.codigo_rol=='ROL_LIC_LABORATORIO'):
        espera_examen=EsperaExamen.objects.filter(fecha__year=fecha_hoy.year, 
                        fecha__month=fecha_hoy.month, 
                        fecha__day=fecha_hoy.day,fase_examenes_lab=EsperaExamen.OPCIONES_FASE[1][0]).select_related('expediente__id_paciente').order_by('numero_cola_laboratorio')
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
        }
        diccionario["numero_cola_laboratorio"]= fila.numero_cola_laboratorio
        diccionario["nombre"]=fila.expediente.id_paciente.nombre_paciente
        diccionario["apellidos"]=fila.expediente.id_paciente.apellido_paciente
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
        resultado=Resultado.objects.get(id_resultado=id_resultado)
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
            response={
                'formset':formset
            }
            return render(request,'laboratorio/resultados.html',response)
        elif request.method=='POST':
            
            if formset.is_valid():
                for i in range(cantidad_parametros):
                    dato=request.POST.get('form-'+str(i)+'-dato')
                    obj, created=ContieneValor.objects.update_or_create(parametro=parametros[i],resultado=resultado,defaults={'dato':dato})
                    
                response={
                    'type':'success',
                    'data':'Guardado!'
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
   
    item.save()
    response={
            'type':'success',
            'data':'Resultados Listos'
        }

    return JsonResponse(response, safe=False)

#Método para descargar examenes de laboratorio
#Método que genera los pdf 
def generar_pdf(request,id_resultado):
    #puede recibir la info como diccionario
    html_string = render_to_string('ResultadosDeLaboratorio.html')
    html = HTML(string=html_string)
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