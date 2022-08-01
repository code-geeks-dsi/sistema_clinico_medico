import json
from django.shortcuts import redirect, render
from django.db.models import Q
from modulo_expediente.serializers import DosisListSerializer, MedicamentoSerializer, PacienteSerializer, ContieneConsultaSerializer
from django.core import serializers
from datetime import datetime
from modulo_expediente.filters import MedicamentoFilter, PacienteFilter
from modulo_expediente.models import (
    Consulta, Dosis, Medicamento, Paciente, ContieneConsulta, Expediente, 
    RecetaMedica, SignosVitales,ConstanciaMedica, ReferenciaMedica)
from modulo_control.models import Enfermera, Empleado, Rol
from .forms import (
    ConsultaFormulario, DatosDelPaciente, DosisFormulario, IngresoMedicamentos, ReferenciaMedicaForm)
from django.http import JsonResponse
from datetime import date
from django.urls import reverse
from urllib.parse import urlencode
from urllib.request import urlopen
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.views import View 
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
# Create your views here.

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
        signosvitales=SignosVitales()
        #signosvitales.enfermera=Enfermera.objects.get(id_enfermera=CODIGO_EMPLEADO)
        signosvitales.save()
        #Creando objeto Consulta
        consulta=Consulta()
        consulta.signos_vitales_id=signosvitales.id_signos_vitales
        consulta.save()
        #receta medica
        receta=RecetaMedica()
        receta.Consulta=consulta
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
def modificar_signosVitales(request, id_signos_vitales):
    datos={
        "empleado":request.user,
        "id_signos":int(id_signos_vitales),
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
    consulta=Consulta.objects.get(signos_vitales_id=id_signos_vitales)
    contieneConsulta=ContieneConsulta.objects.get(consulta_id=consulta.id_consulta)
    contieneConsulta.fase_cola_medica="3"
    contieneConsulta.save()

    return JsonResponse(response, safe=False)

def agregar_medicamento(request):
    idmedicamento=request.GET.get('id', None)
    if request.method == 'GET':
        if idmedicamento==None:
            formulario= IngresoMedicamentos()
        else:     
            medicamento=Medicamento.objects.get(id_medicamento=idmedicamento)
            formulario = IngresoMedicamentos(instance=medicamento)

    else:
        if idmedicamento==None:
            formulario= IngresoMedicamentos(request.POST)
            if  formulario.is_valid():
                new_medicamento=formulario.save()
                messages.add_message(request=request, level=messages.SUCCESS, message="Medicamento registrado con exito")
                # base_url = reverse('agregar_medicamento')
                # query_string =  urlencode({'id': new_medicamento.id_medicamento})
                # url = '{}?{}'.format(base_url, query_string)
                # return redirect(url)
        else:
            medicamento=Medicamento.objects.get(id_medicamento=idmedicamento)
            formulario = IngresoMedicamentos(request.POST, instance=medicamento)
            formulario.save()
            messages.add_message(request=request, level=messages.SUCCESS, message="El Medicamento se ha modificado con exito")
        
    return render(request,"medicamentos.html",{'formulario':formulario})

@login_required
def editar_consulta(request,id_consulta):
    if request.user.roles.codigo_rol =='ROL_DOCTOR':
        contiene_consulta=ContieneConsulta.objects.get(consulta__id_consulta=id_consulta)
        paciente=contiene_consulta.expediente.id_paciente
        signos_vitales=contiene_consulta.consulta.signos_vitales
        consulta=Consulta.objects.get(id_consulta=id_consulta)
        receta=RecetaMedica.objects.get(Consulta=consulta)
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
        datos={
            'paciente':paciente,
            'signos_vitales':signos_vitales,
            'id_consulta':id_consulta,
            'id_receta':receta.id_receta_medica,
            'consulta_form':consulta_form,
            'edad':edad,
            'dosis_form':DosisFormulario(),
            'dosis':dosis
        }
        
        return render(request,"expediente/consulta.html",datos)
    else:
        return render(request,"Control/error403.html")
    
def busqueda_medicamento(request):
    queryset=Medicamento.objects.all()
    result= MedicamentoFilter(request.GET, queryset=queryset)
    medicamento =MedicamentoSerializer(result.qs, many=True)
    if(len(result.qs) ==0):
        response={
            'type':'warning',
            'title':'Error!',
            'data':'El medicamento aún no ha sido registrado'
        }
        return JsonResponse(response)
    return JsonResponse({'data':medicamento.data})
     #la clave tiene que ser data para que funcione con el metodo.

def autocompletado_medicamento(request):
    
    medicamentos=Medicamento.objects.values('nombre_generico',).all()
    medicamentosList=[]
    for medicamento in medicamentos:
        medicamentosList.append(medicamento['nombre_generico'])
    return JsonResponse({"data":medicamentosList})
    #la clave tiene que ser data para que funcione con el metodo

@csrf_exempt
@login_required
def dosis_medicamento(request):
    if request.user.roles.codigo_rol =='ROL_DOCTOR':
        if request.method=='POST':
            medicamento=DosisFormulario(request.POST)
            if medicamento.is_valid():
                medicamento.save()
                dosis=Dosis.objects.filter(receta_medica=request.POST['receta_medica'])
                serializer=DosisListSerializer(dosis, many=True)
                response={
                'type':'success',
                'title':'Guardado!',
                'data':'Dosis Guardada!',
                'dosis':serializer.data
            }
            else:
                response={
                'type':'warning',
                'title':'Error!',
                'data':medicamento.errors,
                'test':""
            }
    else:
        response={
                'type':'warning',
                'title':'Error!',
                'data':'Acceso denegado',
                'test':""
            }
    
    return JsonResponse(response)

#Método que elimina una dosis de la receta medica
@login_required
def eliminar_dosis(request, id_dosis):
    if request.user.roles.codigo_rol =='ROL_DOCTOR':
        try:
            dosis=Dosis.objects.get(id_dosis=id_dosis)
            dosis.delete()
            dosis=Dosis.objects.filter(receta_medica=request.GET['id_receta'])
            serializer=DosisListSerializer(dosis, many=True)
            response={
                'type':'success',
                'title':'Eliminado',
                'data':'Se ha eliminado la dosis de la receta medica',
                'dosis':serializer.data
            }
        except:
            response={
                'type':'warning',
                'title':'Error',
                'data':'La dosis no esta ingresada en la receta medica'
            }
    else:
        response={
                'type':'warning',
                'title':'Error',
                'data':'Acceso denegado'
            }
    return JsonResponse(response, safe=False)

def buscar_expediente(request):
    if request.user.roles.codigo_rol=='ROL_DOCTOR':
        return render(request,"expediente/buscar_expediente.html")
    else:
        return render(request,"Control/error403.html")


class ConstanciaMedicaView(View):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id'] 
        # constancia = ConstanciaMedica.objects.get(id_constancia_medica=id)
        context  = {'id':id}
        return render(request, 'expediente/constancia_medica.html', context)

    def post(self, request, *args, **kwargs): 
        #crear constancia medica
        pass

    def put(self, request, *args, **kwargs): 
        #update constancia medica
        pass

class ConstanciaMedicaCreate(CreateView):
    model = ConstanciaMedica
    template_name = 'expediente/crear_constancia_medica.html'
    fields = ['dias_reposo','fecha_de_emision','consulta','diagnostico_constancia',]
    success_url = reverse_lazy('constancia-medica',
                            kwargs={'id': 1},)

def templete_agenda(request):
    return render(request,"expediente/agenda.html")

class ReferenciaMedicaView(View):
    form_class = ReferenciaMedicaForm
    # initial = {'key': 'value'}s
    template_name = 'expediente/referencia/create_update_referencia_medica.html'

    def get(self, request, *args, **kwargs):
        id_referencia=request.GET.get('id', None)
        if id_referencia!= None:
            initial_data={'id_referencia_medica':int(id_referencia)}
            form = self.form_class( instance=ReferenciaMedica.objects.get(**initial_data))
        else:
            form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        id_consulta=int(self.kwargs['id_consulta']) 
        id_referencia=request.GET.get('id', None)
        #Recupera la url actual
        url=request.get_full_path()
        if id_referencia!= None:
            initial_data={'id_referencia_medica':int(id_referencia)}
            form = self.form_class(request.POST, instance=ReferenciaMedica.objects.get(**initial_data))
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            referencia_medica=form.save(commit=False)
            referencia_medica.consulta=Consulta.objects.get(id_consulta=id_consulta)
            form.save()
            return redirect(url)
    def put(self, request, *args, **kwargs):
        form = self.form_class(request.PUT)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})

    
    
    