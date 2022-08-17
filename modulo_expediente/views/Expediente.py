from django.shortcuts import redirect, render
from modulo_expediente.serializers import PacienteSerializer, ContieneConsultaSerializer
from datetime import datetime
from modulo_expediente.filters import PacienteFilter
from modulo_expediente.models import (
    Consulta, Dosis, Paciente, ContieneConsulta, Expediente, 
    RecetaMedica, SignosVitales,ReferenciaMedica,DocumentoExpediente)
from modulo_control.models import Rol
from ..forms import ( ConsultaFormulario, ControlSubsecuenteform, DatosDelPaciente, DosisFormulario, HojaEvolucionForm, DocumentoExpedienteForm, antecedentesForm)
from django.http import JsonResponse
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.views import View 
from django.views.generic import View, TemplateView
from django.views.generic import TemplateView
from django.http import Http404
import boto3

def busqueda_paciente(request):

    result= PacienteFilter(request.GET, queryset=Paciente.objects.all())
    pacientes =PacienteSerializer(result.qs, many=True)
    return JsonResponse({'data':pacientes.data})
     #la clave tiene que ser data para que funcione con el metodo. 

def autocompletado_apellidos(request):
    
    apellidos=Paciente.objects.values("apellido_paciente").all()
    apellidosList=[]
    for apellido in apellidos:
        apellidosList.append(apellido['apellido_paciente'])
    return JsonResponse({"data":apellidosList})
    #la clave tiene que ser data para que funcione con el metodo. 

@login_required(login_url='/login/')
def sala_consulta(request):
    roles=Rol.objects.values_list('codigo_rol','id_rol').all()
    data={}
    data['titulo']="Sala de Espera"
    data['rol']=request.user.roles.id_rol
    for rol in roles:
        data[rol[0]]=rol[1]
    if request.user.roles.codigo_rol =="ROL_SECRETARIA" or request.user.roles.codigo_rol=="ROL_DOCTOR" or request.user.roles.codigo_rol =="ROL_ENFERMERA":
        return render(request,"expediente/salaEspera.html",data)
    else:
        return render(request,"Control/error403.html", data)


#Metodo que devuelve los datos del paciente en json
@login_required
def get_paciente(request, id_paciente):
    paciente=Paciente.objects.filter(id_paciente=id_paciente)
    serializer=PacienteSerializer(paciente, many= True)
    return JsonResponse(serializer.data, safe=False)
@csrf_exempt
@login_required()
#Metodo que devuelve los datos del objeto contiene consulta en json
def agregar_cola(request, id_paciente):
    #CODIGO_EMPLEADO=1
    expediente=Expediente.objects.get(id_paciente_id=id_paciente)
    idExpediente=expediente.id_expediente
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
        
        #Creando objetos signos vitales

        #signosvitales.enfermera=Enfermera.objects.get(id_enfermera=CODIGO_EMPLEADO)

        #Creando objeto Consulta
        consulta=Consulta()
        consulta.save()
        #Se crean los signos vitales, para que funcione de igual forma la función de actualizar
        SignosVitales.objects.create(consulta=consulta)
        #receta medica
        receta=RecetaMedica()
        receta.consulta=consulta
        receta.save()
        #Creando Objeto contieneCola
        contieneconsulta=ContieneConsulta()
        contieneconsulta.expediente=expediente
        contieneconsulta.numero_cola=numero
        contieneconsulta.consulta_id=consulta.id_consulta
        contieneconsulta.save()
        response={
            'type':'success',
            'title':'Exito',
            'data':'Paciente agregado a la cola'
        }
        return JsonResponse(response, safe=False)

#Metodo que devuelve una lista de constieneConsulta filtrado por la fecha de hoy
def  get_contiene_consulta(request):
    fecha=datetime.now()
    contieneconsulta=ContieneConsulta.objects.filter(fecha_de_cola__year=fecha.year, 
                    fecha_de_cola__month=fecha.month, 
                    fecha_de_cola__day=fecha.day)
    serializer=ContieneConsultaSerializer(contieneconsulta, many=True)
    return JsonResponse(serializer.data, safe=False)

#filtro de contiene consulta para la vista Doctor
def contiene_consulta_con_filtro(request):
    fecha=datetime.now()
    contieneconsulta=ContieneConsulta.objects.filter(fecha_de_cola__year=fecha.year, 
                    fecha_de_cola__month=fecha.month, 
                    fecha_de_cola__day=fecha.day)
    serializer=ContieneConsultaSerializer(contieneconsulta, many=True)
    return JsonResponse(serializer.data, safe=False)

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

#Método que crea un nuevo paciente y lo asigna a un expediente
def crear_expediente(request):
    idpaciente=request.GET.get('id', None)
    if request.method == 'GET':
        if idpaciente==None:
            formulario= DatosDelPaciente()
        else:     
            paciente=Paciente.objects.get(id_paciente=idpaciente)
            formulario = DatosDelPaciente(instance=paciente)

    else:
        if idpaciente==None:
            formulario= DatosDelPaciente(request.POST)
            if  formulario.is_valid():
                new_paciente=formulario.save()
                expediente=Expediente()
                expediente.fecha_creacion_expediente=datetime.now()
                #Generando código expediente
                nombrepaciente = formulario["nombre_paciente"].value()
                apellidopaciente=formulario["apellido_paciente"].value()
                year=datetime.now().date().strftime("%Y")[2:]
                texto=nombrepaciente[0]+apellidopaciente[0]
                texto=texto.lower()#Solo texto en minusculas
                texto=texto+year
                try:
                    correlativo = correlativo = Expediente.objects.filter(codigo_expediente__startswith=texto).last().codigo_expediente
                    correlativo=int(correlativo[4:])
                except:
                    correlativo=0 
                correlativo=correlativo+1
                if correlativo < 10:
                    correlativo="00"+str(correlativo)
                elif correlativo < 100:
                    correlativo = "0"+str(correlativo)
                #Codigo de Usuario al estilo -- mv17012 ---
                codigo=texto+correlativo
                expediente.codigo_expediente=codigo
                idpaciente=list(Paciente.objects.values("id_paciente").all())
                idList=[]
                for i in idpaciente:
                    idList.append(i['id_paciente'])
                expediente.id_paciente_id=idList[-1]
                expediente.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Paciente registrado con exito")
                base_url = reverse('crear_expediente')
                query_string =  urlencode({'id': new_paciente.id_paciente})
                url = '{}?{}'.format(base_url, query_string)
                return redirect(url)
        else:
            paciente=Paciente.objects.get(id_paciente=idpaciente)
            formulario = DatosDelPaciente(request.POST, instance=paciente)
            formulario.save()
            messages.add_message(request=request, level=messages.SUCCESS, message="El Paciente se ha modificado con exito")
        
    return render(request,"datosdelPaciente.html",{'formulario':formulario})

  
@csrf_exempt
def modificar_signosVitales(request, id_consulta):
    datos={
        "empleado":request.user,
        "id_consulta":int(id_consulta),
        "unidad_temperatura":request.POST['unidad_temperatura'],
        "unidad_peso":request.POST['unidad_peso'],
        "valor_temperatura":request.POST['valor_temperatura'],
        "valor_peso":request.POST['valor_peso'],
        "valor_arterial_diasolica":request.POST['valor_presion_arterial_diastolica'],
        "valor_arterial_sistolica":request.POST['valor_presion_arterial_sistolica'],
        "valor_frecuencia_cardiaca":request.POST['valor_frecuencia_cardiaca'],
        "valor_saturacion_oxigeno":request.POST['valor_saturacion_oxigeno'],
    }
    response=SignosVitales.objects.modificar_signos_vitales(datos)
    contieneConsulta=ContieneConsulta.objects.get(consulta__id_consulta=id_consulta)
    contieneConsulta.fase_cola_medica="3"
    contieneConsulta.save()

    return JsonResponse(response, safe=False)


@login_required
def editar_consulta(request,id_consulta):
    if request.user.roles.codigo_rol =='ROL_DOCTOR':
        contiene_consulta=ContieneConsulta.objects.get(consulta__id_consulta=id_consulta)
        paciente=contiene_consulta.expediente.id_paciente
        signos_vitales=SignosVitales.objects.filter(consulta=contiene_consulta.consulta)
        consulta=contiene_consulta.consulta
        receta=RecetaMedica.objects.get(consulta=consulta)
        dosis=Dosis.objects.filter(receta_medica=receta)
        if request.method=='POST':
            consulta_form=ConsultaFormulario(request.POST,instance=consulta)
            if consulta_form.is_valid():
                consulta=consulta_form.save()
                contiene_consulta.fase_cola_medica = '6'
                contiene_consulta.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Consulta Guardada!")
        else:
            consulta_form=ConsultaFormulario(instance=consulta)
        edad = relativedelta(datetime.now(), paciente.fecha_nacimiento_paciente)
        referencias_medicas= ReferenciaMedica.objects.filter(consulta=consulta)
        datos={
            'paciente':paciente,
            'signos_vitales':signos_vitales,
            'id_consulta':id_consulta,
            'id_receta':receta.id_receta_medica,
            'consulta_form':consulta_form,
            'hoja_evolucion_form':HojaEvolucionForm(),
            'edad':edad,
            'dosis_form':DosisFormulario(),
            'dosis':dosis,
            'referencias':referencias_medicas
        }
        
        return render(request,"expediente/consulta.html",datos)
    else:
        return render(request,"Control/error403.html")
    

def buscar_expediente(request):
    if request.user.roles.codigo_rol=='ROL_DOCTOR':
        return render(request,"expediente/buscar_expediente.html")
    else:
        return render(request,"Control/error403.html")



#View Para imprimir Agenda
class AgendaView(TemplateView):
    template_name = "expediente/agenda.html"   

#view Para Consulta
##Para acceder a esto es necesario que el usuario tenga el permiso para editar consulta
class ConsultaView(PermissionRequiredMixin, TemplateView):
    permission_required = ('modulo_expediente.change_consulta')
    template_name = "expediente/consulta.html"
    login_url='/login/'  

    def get(self, request, *args, **kwargs):
        id_consulta=self.kwargs['id_consulta'] 
        try:
            #Consultando Instancias
            contiene_consulta=ContieneConsulta.objects.get(consulta__id_consulta=id_consulta)
            paciente=contiene_consulta.expediente.id_paciente
            expediente=contiene_consulta.expediente.id_expediente
            consulta=contiene_consulta.consulta
            signos_vitales=SignosVitales.objects.filter(consulta=contiene_consulta.consulta)        
            receta=RecetaMedica.objects.get(consulta=consulta)
            dosis=Dosis.objects.filter(receta_medica=receta)
            consulta_form=ConsultaFormulario(instance=consulta)
            edad = relativedelta(datetime.now(), paciente.fecha_nacimiento_paciente)
            referencias_medicas= ReferenciaMedica.objects.filter(consulta=consulta)
            datos={
                'paciente':paciente,
                'signos_vitales':signos_vitales,
                'id_consulta':id_consulta,
                'id_expediente':expediente,
                'id_receta':receta.id_receta_medica,
                'consulta_form':consulta_form,
                'hoja_evolucion_form':HojaEvolucionForm(),
                'control_subsecuente_form':ControlSubsecuenteform(),
                'antecedentes_form':antecedentesForm(instance=contiene_consulta.expediente),
                'edad':edad,
                'dosis_form':DosisFormulario(),
                'dosis':dosis,
                'referencias':referencias_medicas
            }
        except ContieneConsulta.DoesNotExist:
            raise Http404("Consulta no encontrada")
        return render(request, self.template_name, datos)
    
    def post(self, request, *args, **kwargs):
        consulta_form=ConsultaFormulario(request.POST, instance=Consulta.objects.get(id_consulta=self.kwargs['id_consulta']))
        if consulta_form.is_valid():
            consulta=consulta_form.save()
            ContieneConsulta.objects.filter(consulta=consulta).update(fase_cola_medica='6')
            messages.add_message(request=request, level=messages.SUCCESS, message="Consulta Guardada!")
            return redirect(reverse('editar_consulta', kwargs={'id_consulta':consulta.id_consulta}))

    
class CreateControlSubsecuente(View):
        form_class = ControlSubsecuenteform

        def post(self, request, *args, **kwargs):
            id_consulta=int(self.kwargs['id_consulta']) 
            form = self.form_class(request.POST)
            if form.is_valid():
                observacion=form.save(commit=False)
                observacion.fecha=datetime.now()
                observacion.consulta=Consulta.objects.get(id_consulta=id_consulta)
                observacion.save()
                response={
                    'type':'success',
                    'data':'Guardado!'
                }
                return JsonResponse(response)


#Clase para almacenamiento de archivos
##Para esta vista es necesario tener permiso de ver expedientes
class ExamenesExternosCreateView(PermissionRequiredMixin,TemplateView):
    template_name = "expediente/examenes_externos/almacenar_examenes_externos.html"
    permission_required = ('modulo_expediente.view_expediente')
    form_class = DocumentoExpedienteForm
    def get(self, request, *args, **kwargs):
        id_consulta=self.kwargs['id_consulta']
        expediente=ContieneConsulta.objects.filter(consulta__id_consulta=id_consulta).values('expediente','expediente__id_paciente__nombre_paciente').first()
        form = self.form_class()
        #Consultando Archivos
        if expediente!= None:
            archivos=DocumentoExpediente.objects.filter(expediente__id_expediente=expediente['expediente']).order_by('-fecha')
            return render(request, self.template_name, {'form': form, 'consulta': id_consulta, 'archivos':archivos, 'paciente':expediente['expediente__id_paciente__nombre_paciente']})
        else:
            raise Http404("Consulta no encontrada")

    def post(self, request, *args, **kwargs):
        id_consulta=self.kwargs['id_consulta']
        expediente=ContieneConsulta.objects.filter(consulta__id_consulta=id_consulta).first().expediente
        #Recueperando Archivo
        archivo=request.FILES['file']
        cantidad=DocumentoExpediente.objects.filter(titulo__startswith=archivo.name).count()
        #archivo.name=f'{archivo.name} ({cantidad})'
        #Almacenando archivo
        documento=DocumentoExpediente.objects.create(
            titulo= archivo.name,
            documento=archivo,
            expediente=expediente,
            empleado=request.user
        )
        response={
                    'id':documento.id_documento,
                    'fecha':documento.fecha.strftime('%d de %b de %Y a las %I:%M '),
                    'propietario':f'{expediente.id_paciente.nombre_paciente} {expediente.id_paciente.apellido_paciente}'
                }
        return JsonResponse(response)
        #return HttpResponseServerError('PARA Errores')

###Funcion de Prueba para recueperación de archivos s3
##Esto genera una url para accdeder al archivo surante 60 segundos
def storageurl(request, id_documento):
    documentos=DocumentoExpediente.objects.get(id_documento=id_documento)
    client = boto3.client('s3')
    response = client.generate_presigned_url('get_object',Params={'Bucket': 'code-geek-medic',
                                                              'Key': f'static/{documentos.documento}'},
                                         HttpMethod="GET", ExpiresIn=1800) #tiempo en segundos

    return redirect(response)

##class AntecedentesUpdate(View):
  ##  form_class = antecedentesForm
    ##template_name = 'expediente/antecedentes.html'

    ##def get(self, request, *args, **kwargs):
      ##  #Datos del expediente
        ##id_expediente=int(self.kwargs['id_expediente'])
        
def antecedentesUpdate(request, id_expediente):
    expediente = Expediente.objects.get(id_expediente=id_expediente)
    if request.method == 'POST':
        form = antecedentesForm(request.POST, instance=expediente)
        if form.is_valid():
            form.save()
            response={
                'type':'success',
                'data':'Guardado!',
                'antecedentes_personales':form.cleaned_data['antecedentes_personales'],
                'antecedentes_familiares':form.cleaned_data['antecedentes_familiares']
            }

        else:
            response={
                'type':'warning',
                'data':'No se pudo guardar. Intente de nuevo.'
            }
        return JsonResponse(response)

