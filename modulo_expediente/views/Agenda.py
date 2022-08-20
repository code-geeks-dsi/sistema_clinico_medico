#Django
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.utils import timezone
from django.db.models import Q
from django.db.utils import IntegrityError

#Librerias Propias
from modulo_expediente.models import CitaConsulta, HorarioConsulta
from modulo_control.models import Empleado
from ..forms import CitaConsultaForm, CitaConsultaSecretariaForm
from ..serializers import CitaConsultaSerializer

#python
from datetime import datetime, timedelta

#View Para imprimir Agenda
class AgendaView(TemplateView):
    response={'type':'','data':''}
    template_name = "expediente/agenda.html"  
    def get(self, request, *args, **kwargs):
        form=CitaConsultaSecretariaForm()
        #Lista de Doctores
        doctores=Empleado.objects.filter(roles__codigo_rol='ROL_DOCTOR')
        horarios=HorarioConsulta.objects.all()
        form.fields['empleado'].queryset = doctores
        form.fields['empleado'].label="Médico"
        return render(request, self.template_name, {'form':form, 'doctores': doctores, 'horarios':horarios})

    #Crear citas Secretaria
    def post(self, request, *args, **kwargs):
        form = CitaConsultaSecretariaForm(request.POST)
        if form.is_valid():
            form.save()
            self.response['type']='success'
            self.response['data']='Cita Programada'
        else:
            self.response['type']='warning'
            self.response['data']=form.errors.get_json_data()['__all__'][0]['message']
        return JsonResponse(self.response)

class CitaConsultaView(View):
    response={'type':'','data':''}
    #Regresa con json con las citas del mes
    def get(self, request, *args, **kwargs):
        start=request.GET['start']
        fecha_inicio=datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
        fecha_inicio=fecha_inicio+timedelta(weeks=3)
        citas=CitaConsulta.objects.filter(fecha_cita__year=fecha_inicio.year, fecha_cita__month=fecha_inicio.month)
        serializer=CitaConsultaSerializer(citas, many= True)
        return JsonResponse(serializer.data, safe=False)

    #Crear citas Doctor
    def post(self, request, *args, **kwargs):
        id_expediente=self.kwargs['id_expediente'] 
        form = CitaConsultaForm(request.POST)
        if form.is_valid():
            cita=form.save(commit=False)
            try:
                cita.empleado=request.user
                cita.save()
                self.response['type']='success'
                self.response['data']='Cita Programada'
            except IntegrityError:
                self.response['type']='warning'
                self.response['data']='Ya tiene una cita programada en el horario seleccionado.'
        else:
            self.response['type']='warning'
            self.response['data']='Ya tiene una cita programada en el horario seleccionado.'

        return JsonResponse(self.response)

class CitaConsultaUpdate(View):
    #Regresa con json con las citas del mes
    def get(self, request, *args, **kwargs):
        try:
            id_cita=self.kwargs['id_cita_consulta'] 
            cita=CitaConsulta.objects.get(id_cita_consulta=id_cita)
            datos_cita={
                'paciente':f'{cita.expediente.id_paciente.nombre_paciente} {cita.expediente.id_paciente.apellido_paciente}',
                'doctor':f'{cita.empleado.nombres} {cita.empleado.apellidos}',
                'id_doctor':f'{cita.empleado.codigo_empleado}',
                'observacion':cita.observacion,
                'fecha':cita.fecha_cita.strftime("%Y-%m-%d"),
                'horario':cita.horario.id_horario,
                'hora':cita.horario.hora_inicio.strftime("%I:%M %p")
            }
            response={
                'type':'success',
                'cita':datos_cita,
            }
        except CitaConsulta.DoesNotExist:
            response={
                'type':'Error'
            }
        return JsonResponse(response)
    def post(self, request, *args, **kwargs):
        response={'type':'warning','data':''}
        try:
            #Recuperando Datos
            id_cita=self.kwargs['id_cita_consulta']
            id_doctor=request.POST['update_medico']
            id_horario=request.POST['update_cita_horario']
            fecha=datetime.strptime(request.POST['update_cita_fecha'], '%Y-%m-%d')
            CitaConsulta.objects.filter(id_cita_consulta=id_cita).update(empleado=id_doctor, horario=id_horario, fecha_cita=fecha)

            response['type']='success'
            response['data']='Cita actualizada.'
        except CitaConsulta.DoesNotExist:
            response['data']='No fue posible actualizar'
        except IntegrityError:
                response['data']='El medico seleccionado tiene una cita programada.'
        return JsonResponse(response)