#Django
from email.mime import image
from django.views.generic import ListView
from django.views import View
from django.shortcuts import (render,redirect)
#Propias
from modulo_expediente.models import TipoConsulta
from modulo_publicidad.forms import PublicacionForm, ServicioImagenForm, ServicioMedicoForm
from modulo_publicidad.models import *

class ServiciosMedicosListView(ListView):
    model=ServicioMedico
    paginate_by = 10
    template_name= "servicios/medicos/lista.html"

class crearServicioMedico(View):
    template_name="servicios/medicos/crear_editar.html"

    def get(self, request, *args, **kwargs):
        data={
            'formServicioMedico':ServicioMedicoForm(),
            'formImagen':ServicioImagenForm()
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
        formImagen=ServicioImagenForm(request.POST,  request.FILES)
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
                    return redirect('editar_servicio_medico', servicio.id_servicio)

        else:
            data={
                'formServicioMedico':formServicioMedico,
                'formImagen':formImagen
            }
            return render(request, self.template_name, data)
class editarServicioMedico(View):
    template_name="servicios/medicos/crear_editar.html"
    def get(self, request, *args, **kwargs):
        id_servicio=kwargs.get('id_servicio', None)
        if id_servicio:
            servicio=Servicio.objects.get(id_servicio=id_servicio)

            data={
                'formServicioMedico':ServicioMedicoForm(instance=servicio),
                'formImagen':ServicioImagenForm()
            }
            return render(request, self.template_name, data)
    def post(self, request, *args, **kwargs):
        '''
        Pasos:
        1. Guardar tipo consulta si existe(Checkbox crear_tipo_consulta). LISTO
        2. Guardar Servicio.LISTO
        3. Guardar Servicio Médico y asignarle servicio.LISTO
        4. Guardar publicación y asignarle el servicio médico.
        5. Guardar Imagen y asignarle la publicación.
        '''
        # Recuperando datos
        formServicioMedico=ServicioMedicoForm(request.POST)
        formPublicacion=PublicacionForm(request.POST)
        formImagen=ServicioImagenForm(request.POST)
        if formServicioMedico.is_valid():
            if formPublicacion.is_valid():
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
                    publicacion=formPublicacion.save(commit=False)
                    publicacion.servicio=servicio
                    publicacion.save()
                    #PASO 5
                    imagen=formImagen.save(commit=False)
                    imagen.publicacion=publicacion
                    imagen.save()




        data={
            'formServicioMedico':formServicioMedico,
            'formPublicacion':formPublicacion,
            'formImagen':formImagen
        }
        return render(request, self.template_name, data)