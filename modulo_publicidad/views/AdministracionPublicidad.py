#Python

#Django
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.forms import modelformset_factory

#Propias
from modulo_publicidad.models import *
from modulo_publicidad.forms import (PublicacionForm,PublicacionImagenForm)

##La url de esta pagina se invoca desde el archivo principal de url
class InicioPublicidad(TemplateView):
    template_name = "publicidad/administracion/inicio.html"

class ClinicaPublicidad(TemplateView):
    template_name = "publicidad/administracion/inicio.html"

# Publicaciones
class CrearPromocion(View):
    template_name = "publicidad/administracion/crearEditar.html"
    ImagenFormSet = modelformset_factory(Imagen, form=PublicacionImagenForm, max_num=3, extra=3)

    def get(self, request, *args, **kwargs):
        form = PublicacionForm()
        form_imagenes=self.ImagenFormSet()
        return render(request, self.template_name, {'form': form, 'formset_imagen': form_imagenes})

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         # <process form cleaned data>
    #         return HttpResponseRedirect('/success/')

    #     return render(request, self.template_name, {'form': form})
    # template_name = "publicidad/administracion/crearEditar.html"
    # form_publicacion = PublicacionForm
    # form_imagen = PublicacionImagenForm
    # # initial = {'key': 'value'}

    # def get(self, request, *args, **kwargs):
    #     form = self.form_publicacion(initial=self.initial)
    #     return render(request, self.template_name, {'form': form})

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         # <process form cleaned data>
    #         return HttpResponseRedirect('/success/')

    #     return render(request, self.template_name, {'form': form})
    

class EditarPromocion(TemplateView):
    template_name = "publicidad/administracion/crearEditar.html"

class PublicacionListView(ListView):
    model=Publicacion
    template_name= "publicidad/administracion/lista.html"