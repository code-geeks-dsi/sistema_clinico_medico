#Django
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.views.generic import ListView
from django.views import View
from django.shortcuts import (render,redirect)
#Propias
from modulo_expediente.models import TipoConsulta
from modulo_publicidad.forms import ServicioImagenForm, ServicioMedicoForm
from modulo_publicidad.models import *

class ServiciosLaboratorioListView(ListView):
    model=ServicioLaboratorioClinico
    paginate_by = 10
    template_name= "servicios/laboratorio/lista.html"

class EliminarServicioLaboratorioView(DeleteView):
    model = Servicio
    template_name= "servicios/laboratorio/confirmar_eliminar.html"
    success_url = reverse_lazy('lista_servicios_medicos')

class CrearServicioLaboratorio(View):
    template_name="servicios/laboratorio/crear_editar.html"

    def get(self, request, *args, **kwargs):
        data={
            'formServicioMedico':ServicioMedicoForm(),
            'formImagen':ServicioImagenForm(),
            'mensajes':[]
        }
        return render(request, self.template_name, data)
    def post(self, request, *args, **kwargs):
        '''
        Pasos:
        1. Guardar tipo consulta si existe(Checkbox crear_tipo_consulta). LISTO
        2. Guardar Servicio.LISTO
        3. Guardar Servicio Médico y asignarle servicio.LISTO
        4. Guardar Imagen y asignarle el servicio.
        '''
        # Recuperando datos
        formServicioLaboratorio=ServicioMedicoForm(request.POST)
        formImagen=ServicioImagenForm(request.POST, request.FILES)

        if formServicioLaboratorio.is_valid():
                if formImagen.is_valid():
                    #PASO 1
                    crear_tipo_consulta=formServicioLaboratorio.cleaned_data['crear_tipo_consulta']  
                    if crear_tipo_consulta==True:
                        nombreTipoConsulta=formServicioLaboratorio.cleaned_data['otro']
                        tipoConsulta=TipoConsulta(nombre=nombreTipoConsulta)
                        tipoConsulta.save()
                    else:
                        tipoConsulta=formServicioLaboratorio.cleaned_data['area'] 
                    #PASO 2
                    servicio=formServicioLaboratorio.save()
                    #PASO 3
                    servicioLaboratorio=ServicioMedico(servicio=servicio,tipo_consulta=tipoConsulta)
                    servicioLaboratorio.save()
                    #PASO 4
                    imagen=formImagen.save(commit=False)
                    imagen.servicio=servicio
                    imagen.save()
                    request.session['mensajes']=[{
                        'type':'success',
                        'data':'Servicio Médico '+servicio.nombre+' Guardado'
                        }]
                    return redirect('editar_servicio_medico',servicio.id_servicio)

        else:
            data={
                'formServicioMedico':formServicioLaboratorio,
                'formImagen':formImagen
            }
            return render(request, self.template_name, data)
class EditarServicioLaboratorio(View):
    template_name="servicios/laboratorio/crear_editar.html"
    def get(self, request, *args, **kwargs):
        id_servicio=kwargs.get('id_servicio', None)
        mensajes=request.session.get('mensajes', [])
        request.session['mensajes']=[]
        servicio=Servicio.objects.get(id_servicio=id_servicio)
        imagen=ImagenServicio.objects.get(servicio=servicio)
        servicioLaboratorio=ServicioMedico.objects.get(servicio=servicio)
        initial_data={
            "area":servicioLaboratorio.tipo_consulta
        }
        servicioLaboratorioForm=ServicioMedicoForm(instance=servicio, initial=initial_data)
        data={
            'formServicioMedico':servicioLaboratorioForm,
            'formImagen':ServicioImagenForm(instance=imagen),
            'mensajes': mensajes
        }
        return render(request, self.template_name, data)
    def post(self, request, *args, **kwargs):
        id_servicio=kwargs.get('id_servicio', None)
        servicio=Servicio.objects.get(id_servicio=id_servicio)
        imagen=ImagenServicio.objects.get(servicio=servicio)
        # Recuperando datos
        formServicioLaboratorio=ServicioMedicoForm(request.POST,instance=servicio)
        formImagen=ServicioImagenForm(request.POST, request.FILES, instance=imagen)
        if formServicioLaboratorio.is_valid():
                if formImagen.is_valid():
                    #PASO 1
                    crear_tipo_consulta=formServicioLaboratorio.cleaned_data['crear_tipo_consulta']  
                    if crear_tipo_consulta==True:
                        nombreTipoConsulta=formServicioLaboratorio.cleaned_data['otro']
                        tipoConsulta=TipoConsulta(nombre=nombreTipoConsulta)
                        tipoConsulta.save()
                    else:
                        tipoConsulta=formServicioLaboratorio.cleaned_data['area'] 
                    #PASO 2
                    servicio=formServicioLaboratorio.save()
                    #PASO 3
                    servicioLaboratorio=ServicioMedico.objects.get(servicio=servicio)
                    servicioLaboratorio.tipo_consulta=tipoConsulta
                    servicioLaboratorio.save()
                    #PASO 4
                    formImagen.save()
                    request.session['mensajes']=[{
                        'type':'success',
                        'data':'Servicio Médico '+servicio.nombre+' Modificado'
                        }] 
                    return redirect(
                        'editar_servicio_medico', 
                        servicio.id_servicio )
        else:
            data={
                'formServicioMedico':formServicioLaboratorio,
                'formImagen':formImagen
            }
            return render(request, self.template_name, data)