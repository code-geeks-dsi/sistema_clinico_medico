import datetime
from django.forms import formset_factory
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from modulo_control.models import Empleado, LicLaboratorioClinico
from modulo_expediente.models import Expediente, Paciente
from modulo_laboratorio.forms import ContieneValorForm
from modulo_laboratorio.models import Categoria, ContieneValor, EsperaExamen, ExamenLaboratorio, Parametro, RangoDeReferencia, Resultado
from modulo_laboratorio.serializers import Examenserializer, ResultadoSerializer
from dateutil.relativedelta import relativedelta
from weasyprint import HTML
from django.http import HttpResponse,JsonResponse, QueryDict
from django.template.loader import render_to_string
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from modulo_laboratorio.views.EsperaExamen import verificar_fase_orden_laboratorio
import tempfile
from django.db.utils import IntegrityError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def sync_cola():
    channel_layer = get_channel_layer()
    colas=['cola_de_resultados_por_orden_de_laboratorio','cola_ordenes','cola_de_resultados']
    for cola in colas:
        async_to_sync(channel_layer.group_send)(
            cola,
            {
                'type': cola
            }
        )
        print(cola+" executada")


@method_decorator(csrf_exempt, name='dispatch')
class ResultadoView(View):
    template_name = 'laboratorio/OrdenExamen/GestionOrdenExamenes.html'
    response={'type':'','data':'', 'info':''}
    #Imprimir en pantalla el formulario de creación de orden
    def get(self, request, *args, **kwargs):
        ##Datos de la consulta
        id_paciente=int(self.kwargs['id_paciente'])
        id_orden=int(self.kwargs['id_orden'])
        # id_receta_examen=int(self.kwargs['id_receta_examen'])
        # contiene_consulta=ContieneConsulta.objects.get(consulta__id_consulta=id_consulta)
        categorias=Categoria.objects.all()
        paciente=Paciente.objects.get(id_paciente=id_paciente)
        edad = relativedelta(datetime.now(), paciente.fecha_nacimiento_paciente)
        resultados=Resultado.objects.filter(orden_de_laboratorio=id_orden)
        return render(request, self.template_name, {'Categoria':categorias, 'paciente':paciente, 'edad': edad, 'item_recetas':resultados,'id_orden':id_orden})
    
    #Actualizando/Se agregan items a la orden de examen
    def put(self, request, *args, **kwargs):
        id_paciente=int(self.kwargs['id_paciente'])
        id_orden=int(self.kwargs['id_orden'])
        data = QueryDict(request.body)
        self.response['mensajes']=[]
        try:
            item=Resultado.create(
                id_examen=data['id_examen'],
                id_orden=id_orden
            )
            item.save()
            examen=ResultadoSerializer(item)
            numero=Resultado.objects.filter(orden_de_laboratorio=id_orden).count()

            self.response['mensajes'].append({
                'type':'success',
                'title':'Examen agregado!',
                'data':'Examen agregado!'
                })
            self.response['info']={
                'id_resultado':item.id_resultado,
                'numero': numero,
                'examen': examen.data
            }
        except IntegrityError:
            self.response['mensajes'].append({
                'type':'warning',
                'title':'Examen ya existe',
                'data':'El examen ya existe en la orden.'
                })
            # no hay necesidad de actualizar cola porque no hubo cambio
            return JsonResponse(self.response, status=500)
        orden=item.orden_de_laboratorio
        print(self.response['mensajes'])
        orden_en_proceso_mensaje=verificar_fase_orden_laboratorio(orden)
        if(orden_en_proceso_mensaje!=None):
            self.response['mensajes'].append(orden_en_proceso_mensaje)
        print(self.response['mensajes'])
        sync_cola()
        return JsonResponse(self.response)

    ##Para eliminar
    def delete(self, request, *args, **kwargs):
        id_orden=int(self.kwargs['id_orden'])
        self.response['mensajes']=[]
        data = QueryDict(request.body)
        resultado=Resultado.objects.filter(
            id_resultado=data['id_resultado']
        ).first()
        orden=resultado.orden_de_laboratorio
        if (resultado.fase_examenes_lab==Resultado.OPCIONES_FASE[1][0]):
            self.response['mensajes'].append({
                'type':'error',
                'title':'No se puede eliminar, porque la muestra ya ha sido entregada',
                'data':'Examen No Eliminado!'
                })
        else:
            resultado.delete()
            self.response['mensajes'].append({
                'type':'success',
                'title':'Examen Eliminado!',
                'data':'El examen ha sido eliminado'
                })
            orden=resultado.orden_de_laboratorio
            orden_en_proceso_mensaje=verificar_fase_orden_laboratorio(orden)
            if(orden_en_proceso_mensaje!=None):
                self.response['mensajes'].append(orden_en_proceso_mensaje)
            sync_cola()
        
        # # actualizando las ordenes
        # recetasItems=Resultado.objects.filter(orden_de_laboratorio=id_orden)
        # recetasItems=ResultadoSerializer(recetasItems, many=True)
        # self.response['info']=[]

        return JsonResponse(self.response)

'''
Modificacion: Andrea Monterrosa
Descripcion: Cambiar fase orden de examen
''' 
@csrf_exempt
def cambiar_fase_a_en_proceso(request):
    id_resultado=request.POST.get('id_resultado',0)
    response={
        'mensajes':[]
    }
    try:
        item=Resultado.objects.get(id_resultado=id_resultado)
        item.fase_examenes_lab=Resultado.OPCIONES_FASE[1][0]
        item.fecha_hora_toma_de_muestra=datetime.now()
        item.save()
        response['mensajes'].append({
            'type':'success',
            'title':'Muestra Entregada!',
            'data':'Examen en proceso'
            })
        orden=item.orden_de_laboratorio
        orden_en_proceso_mensaje=verificar_fase_orden_laboratorio(orden)
        if(orden_en_proceso_mensaje!=None):
            response['mensajes'].append(orden_en_proceso_mensaje)
        sync_cola()
    except:
        response['mensajes'].append({
        'type':'error',
        'title':'Intente de Nuevo!',
        'data':'No se pudo cambiar de fase'
        })

    # actualizando las ordenes
    # ordenes=Resultado.objects.filter(orden_de_laboratorio=orden)
    # ordenes=ResultadoSerializer(ordenes, many=True)
    # response['info']=ordenes.data

    return JsonResponse(response, safe=False)

# Lic de Laboratorio
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
    # cambiando la fase de la orden
    orden=item.orden_de_laboratorio
    orden_en_proceso_mensaje=verificar_fase_orden_laboratorio(orden)

    # if(orden_en_proceso_mensaje!=None):
        # self.response['mensajes'].append(orden_en_proceso_mensaje)

    sync_cola()
    return JsonResponse(response, safe=False)

def elaborar_resultados_examen(request,id_resultado):
        data={} 
        lic_laboratorio=LicLaboratorioClinico.objects.get(empleado=request.user)
        resultado=Resultado.objects.get(id_resultado=id_resultado)
        resultado.lic_laboratorio=lic_laboratorio
        resultado.save()
        # verificando si los resultados han sido entregados
        espera_examen=resultado.orden_de_laboratorio

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
            paciente= espera_examen.expediente.id_paciente
            edad = relativedelta(datetime.now(), paciente.fecha_nacimiento_paciente)
            response={
                'formset':formset,
                'nombre_examen':examen.nombre_examen,
                'paciente':paciente,
                'edad':edad,
                'cantidad_valores':len(valores),
                'fase':resultado.fase_examenes_lab
            }
            return render(request,'laboratorio/resultados.html',response)
        elif request.method=='POST':
            #Si el examen esta listo
            if (espera_examen.fase_examenes_lab==EsperaExamen.OPCIONES_FASE_ORDEN[0][0] 
            or espera_examen.fase_examenes_lab==EsperaExamen.OPCIONES_FASE_ORDEN[2][0]
            or espera_examen.fase_examenes_lab==EsperaExamen.OPCIONES_FASE_ORDEN[3][0]):
                response={
                    'type':'info',
                    'title':'No tiene permisos para editar',
                    'data':'No se pueden modificar los examenes de laboratorio, porque ya fueron entregados.'
                }
            #Los examenes listos no se pueden mdificar    
            #Fin de la validación     
            elif formset.is_valid():
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

# generar pdf consolidado
#Método para descargar examenes de laboratorio
#Método que genera los pdf 
def generar_orden_pdf(request,orden_id):
    data={}
    orden_examenes=EsperaExamen.objects.get(id=orden_id)

    # actualizando la fase de los resultados
    Resultado.objects.filter(orden_de_laboratorio=orden_examenes).update(fase_examenes_lab=Resultado.OPCIONES_FASE[3][0])

    # actualizando la fase de la orden
    orden_examenes.fase_examenes_lab=EsperaExamen.OPCIONES_FASE_ORDEN[3][0]
    orden_examenes.save()
    sync_cola()

    #consultando datos del paciente
    idExpediente=orden_examenes.expediente_id
    expediente=Expediente.objects.get(id_expediente=idExpediente)
    idpaciente=expediente.id_paciente_id
    paciente=Paciente.objects.get(id_paciente=idpaciente)
    edad = relativedelta(datetime.now(), paciente.fecha_nacimiento_paciente)
    #consultando datos de los examenes
    resultados=Resultado.objects.filter(orden_de_laboratorio_id=orden_id)
    lista=[]
    for i in range(len(resultados)):
        resultado={
            'id_resultado':"",
            'id_examen':"",
            'fecha_de_elaboracion':"",
            'contieneValor':"",
            'parametros':"",
            'referencias':"",
            'licdeLab':"",
            'empleado':"",
        }
        resultado['id_resultado']=resultados[i].id_resultado
        examen=ExamenLaboratorio.objects.get(id_examen_laboratorio=resultados[i].examen_laboratorio_id)
        examen=Examenserializer(examen , many=False)
        resultado['examenlab']=examen.data
        resultado['fecha_de_elaboracion']=resultados[i].fecha_hora_elaboracion_de_reporte
        resultado['contieneValor']=ContieneValor.objects.filter(resultado_id=resultados[i].id_resultado)
        parametro=ContieneValor.objects.filter(resultado_id=resultados[i].id_resultado).values('parametro').distinct()
        resultado['parametros']=parametro
        resultado['referencias']=RangoDeReferencia.objects.filter(parametro__in=parametro)
        licDeLab=LicLaboratorioClinico.objects.get(id_lic_laboratorio=resultados[i].lic_laboratorio_id)
        resultado['empleado']=Empleado.objects.get(codigo_empleado=licDeLab.empleado_id)

        lista.append(resultado)
    data={ 'paciente':paciente,'edad':edad,'resultados':lista}
    #puede recibir la info como diccionario
    html_string = render_to_string('OrdenDeExamenes.html',data)
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


# generar pdf de un resultado
def generar_resultado_pdf(request,id_resultado):
    data={}
    
    #consultando datos del paciente
    resultado=Resultado.objects.get(id_resultado=id_resultado)

    # actualizando la fase del resultado
    resultado.fase_examenes_lab=Resultado.OPCIONES_FASE[3][0]
    resultado.save()

    # Cambiando fase de orden de laboratorio
    orden=resultado.orden_de_laboratorio
    orden_en_proceso_mensaje=verificar_fase_orden_laboratorio(orden)
    # if(orden_en_proceso_mensaje!=None):
    #     response['mensajes'].append(orden_en_proceso_mensaje)
    sync_cola()
    expediente=resultado.orden_de_laboratorio.expediente
    paciente=expediente.id_paciente
    edad = relativedelta(datetime.now(), paciente.fecha_nacimiento_paciente)
    #consultando datos del examen
    examenlab=resultado.examen_laboratorio
    fecha=resultado.fecha_hora_elaboracion_de_reporte
    #Consultando datos del encargado de emitir examen
    licdeLab=resultado.lic_laboratorio
    # codigo_empleado=licdeLab.empleado_id
    empleado=licdeLab.empleado
    #Consultando resultados
    contieneValor=ContieneValor.objects.filter(resultado_id=id_resultado)
    parametros=ContieneValor.objects.filter(resultado_id=id_resultado).values('parametro').distinct()
    referencias=RangoDeReferencia.objects.filter(parametro__in=parametros)
    
    data={'contieneValor':contieneValor, 'paciente':paciente,'edad':edad,'fecha':fecha,'empleado':empleado,'examenlab':examenlab,'referencias':referencias}
    #puede recibir la info como diccionario
    html_string = render_to_string('ResultadoLaboratorio.html',data)
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