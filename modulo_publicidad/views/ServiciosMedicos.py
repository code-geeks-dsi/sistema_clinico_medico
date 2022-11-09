#Django
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.views.generic import ListView
from django.views import View
from django.shortcuts import (render,redirect,reverse)
#Propias
from modulo_expediente.models import TipoConsulta
from modulo_publicidad.forms import ServicioImagenForm, ServicioMedicoForm
from modulo_publicidad.models import *

class ServiciosMedicosListView(ListView):
    model=ServicioMedico
    paginate_by = 10
    template_name= "servicios/medicos/lista.html"

class EliminarServicioMedicoView(DeleteView):
    model = Servicio
    template_name= "servicios/medicos/confirmar_eliminar.html"
    success_url = reverse_lazy('lista_servicios_medicos')

class CrearServicioMedico(View):
    template_name="servicios/medicos/crear_editar.html"

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
        formServicioMedico=ServicioMedicoForm(request.POST)
        formImagen=ServicioImagenForm(request.POST, request.FILES)

        if formServicioMedico.is_valid():
                if formImagen.is_valid():
                    #PASO 1
                    crear_tipo_consulta=formServicioMedico.cleaned_data['crear_tipo_consulta']  
                    if crear_tipo_consulta==True:
                        nombreTipoConsulta=formServicioMedico.cleaned_data['otro']
                        tipoConsulta=TipoConsulta(nombre=nombreTipoConsulta)
                        tipoConsulta.save()
                    else:
                        tipoConsulta=formServicioMedico.cleaned_data['area'] 
                    #PASO 2
                    servicio=formServicioMedico.save()
                    #PASO 3
                    servicioMedico=ServicioMedico(servicio=servicio,tipo_consulta=tipoConsulta)
                    servicioMedico.save()
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
                'formServicioMedico':formServicioMedico,
                'formImagen':formImagen
            }
            return render(request, self.template_name, data)
class EditarServicioMedico(View):
    template_name="servicios/medicos/crear_editar.html"
    def get(self, request, *args, **kwargs):
        id_servicio=kwargs.get('id_servicio', None)
        mensajes=request.session.get('mensajes', [])
        servicio=Servicio.objects.get(id_servicio=id_servicio)
        imagen=ImagenServicio.objects.get(servicio=servicio)
        servicioMedico=ServicioMedico.objects.get(servicio=servicio)
        initial_data={
            "area":servicioMedico.tipo_consulta
        }
        servicioMedicoForm=ServicioMedicoForm(instance=servicio, initial=initial_data)
        data={
            'formServicioMedico':servicioMedicoForm,
            'formImagen':ServicioImagenForm(instance=imagen),
            'mensajes': mensajes
        }
        return render(request, self.template_name, data)
    def post(self, request, *args, **kwargs):
        id_servicio=kwargs.get('id_servicio', None)
        servicio=Servicio.objects.get(id_servicio=id_servicio)
        imagen=ImagenServicio.objects.get(servicio=servicio)
        # Recuperando datos
        formServicioMedico=ServicioMedicoForm(request.POST,instance=servicio)
        formImagen=ServicioImagenForm(request.POST, request.FILES, instance=imagen)
        if formServicioMedico.is_valid():
                if formImagen.is_valid():
                    #PASO 1
                    crear_tipo_consulta=formServicioMedico.cleaned_data['crear_tipo_consulta']  
                    if crear_tipo_consulta==True:
                        nombreTipoConsulta=formServicioMedico.cleaned_data['otro']
                        tipoConsulta=TipoConsulta(nombre=nombreTipoConsulta)
                        tipoConsulta.save()
                    else:
                        tipoConsulta=formServicioMedico.cleaned_data['area'] 
                    #PASO 2
                    servicio=formServicioMedico.save()
                    #PASO 3
                    servicioMedico=ServicioMedico.objects.get(servicio=servicio)
                    servicioMedico.tipo_consulta=tipoConsulta
                    servicioMedico.save()
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
                'formServicioMedico':formServicioMedico,
                'formImagen':formImagen
            }
            return render(request, self.template_name, data)