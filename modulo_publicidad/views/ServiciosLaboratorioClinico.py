#Django
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.views.generic import ListView
from django.views import View
from django.shortcuts import (render,redirect)
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

#Propias
from modulo_expediente.models import TipoConsulta
from modulo_laboratorio.models import ExamenLaboratorio
from modulo_publicidad.forms import ServicioImagenForm, ServicioLaboratorioForm
from modulo_publicidad.models import *

class ServiciosLaboratorioListView(ListView):
    model=ServicioLaboratorioClinico
    paginate_by = 10
    template_name= "servicios/laboratorio/lista.html"

class EliminarServicioLaboratorioView(DeleteView):
    model = Servicio
    template_name= "servicios/laboratorio/confirmar_eliminar.html"
    success_url = reverse_lazy('lista_servicios_laboratorio')

class CrearServicioLaboratorio(View):
    template_name="servicios/laboratorio/crear_editar.html"

    def get(self, request, *args, **kwargs):
        data={
            'formServicioLaboratorio':ServicioLaboratorioForm(),
            'formImagen':ServicioImagenForm(),
            'mensajes':[]
        }
        return render(request, self.template_name, data)
    def post(self, request, *args, **kwargs):
        '''
        Pasos:
        1. Guardar tipo consulta si existe(Checkbox crear_tipo_consulta). LISTO
        2. Guardar Servicio.LISTO
        3. Guardar Servicio de Laboratorio Clínico y asignarle servicio.LISTO
        4. Guardar Imagen y asignarle el servicio.
        '''
        # Recuperando datos
        formServicioLaboratorio=ServicioLaboratorioForm(request.POST)
        formImagen=ServicioImagenForm(request.POST, request.FILES)

        if formServicioLaboratorio.is_valid():
                if formImagen.is_valid():
                    #PASO 2
                    servicio=formServicioLaboratorio.save()
                    #PASO 3
                    try:
                        examen_laboratorio=formServicioLaboratorio.cleaned_data['examen_laboratorio']   
                        servicioLaboratorio=ServicioLaboratorioClinico(examen_laboratorio=examen_laboratorio,servicio=servicio)
                        servicioLaboratorio.save()
                        #PASO 4
                        imagen=formImagen.save(commit=False)
                        imagen.servicio=servicio
                        imagen.save()
                        request.session['mensajes']=[{
                            'type':'success',
                            'data':'Servicio de Laboratorio Clínico '+servicio.nombre+' Guardado'
                            }]
                        return redirect('editar_servicio_laboratorio',servicio.id_servicio)
                    except IntegrityError:
                        request.session['mensajes']=[{
                        'type':'warning',
                        'data':'Servicio de Laboratorio Clínico '+servicio.nombre+' ya existe.'
                        }]
                        servicio.delete()
           
        data={
            'formServicioLaboratorio':formServicioLaboratorio,
            'formImagen':formImagen,
            'mensajes':request.session['mensajes']
        }
        return render(request, self.template_name, data)
        
class EditarServicioLaboratorio(View):
    template_name="servicios/laboratorio/crear_editar.html"
    def get(self, request, *args, **kwargs):
        id_servicio=kwargs.get('id_servicio', None)
        mensajes=request.session.get('mensajes', [])
        if request.session.get('mensajes') is not None:
            del request.session['mensajes']
        servicio=get_object_or_404(Servicio, id_servicio=id_servicio)
        try:
            imagen=ImagenServicio.objects.get(servicio=servicio)
            formImagen=ServicioImagenForm(instance=imagen)
        except ImagenServicio.DoesNotExist:
            formImagen=ServicioImagenForm()

        servicioLaboratorio=ServicioLaboratorioClinico.objects.get(servicio=servicio)
        initial_data={
            "examen_laboratorio":servicioLaboratorio.examen_laboratorio
        }
        servicioLaboratorioForm=ServicioLaboratorioForm(instance=servicio, initial=initial_data)

        data={
            'formServicioLaboratorio':servicioLaboratorioForm,
            'formImagen':formImagen,
            'mensajes': mensajes
        }
        return render(request, self.template_name, data)
    def post(self, request, *args, **kwargs):
        id_servicio=kwargs.get('id_servicio', None)
        servicio=get_object_or_404(Servicio, id_servicio=id_servicio)
        try:
            imagen=ImagenServicio.objects.get(servicio=servicio)
            formImagen=ServicioImagenForm(request.POST, request.FILES, instance=imagen)
        except ImagenServicio.DoesNotExist:
            formImagen=ServicioImagenForm(request.POST, request.FILES)
        # Recuperando datos
        formServicioLaboratorio=ServicioLaboratorioForm(request.POST,instance=servicio)
        if formServicioLaboratorio.is_valid():
                if formImagen.is_valid():
                    #PASO 2
                    servicio=formServicioLaboratorio.save()
                    #PASO 3
                    try:
                        examen_laboratorio=formServicioLaboratorio.cleaned_data['examen_laboratorio']   
                        servicioLaboratorio=ServicioLaboratorioClinico.objects.get(servicio=servicio)
                        servicioLaboratorio.examen_laboratorio=examen_laboratorio
                        servicioLaboratorio.save()
                        #PASO 4
                        imagen=formImagen.save(commit=False)
                        imagen.servicio=servicio
                        imagen.save()
                        request.session['mensajes']=[{
                            'type':'success',
                            'data':'Servicio de Laboratorio Clínico '+servicio.nombre+' Modificado'
                            }] 
                        return redirect(
                            'editar_servicio_laboratorio', 
                            servicio.id_servicio )
                    except IntegrityError:
                        request.session['mensajes']=[{
                        'type':'warning',
                        'data':'Servicio de Laboratorio Clínico '+servicio.nombre+' ya existe.'
                        }]
                        # servicio.delete()
        mensajes=request.session.get('mensajes', [])
        if request.session.get('mensajes') is not None:
            del request.session['mensajes']
        data={
            'formServicioLaboratorio':formServicioLaboratorio,
            'formImagen':formImagen,
            'mensajes': mensajes
        }
        return render(request, self.template_name, data)
           