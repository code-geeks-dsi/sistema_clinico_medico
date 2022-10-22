#Python

#Django
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.forms import modelformset_factory

#Propias
from modulo_publicidad.models import *
from modulo_publicidad.forms import (DescuentoForm, PublicacionForm,PublicacionImagenForm)

##La url de esta pagina se invoca desde el archivo principal de url
class InicioPublicidad(TemplateView):
    template_name = "publicidad/administracion/inicio.html"

class ClinicaPublicidad(TemplateView):
    template_name = "publicidad/administracion/inicio.html"

# Publicaciones
class CrearPromocion(View):
    template_name = "publicidad/administracion/crearEditar.html"
    ImagenFormSet = modelformset_factory(ImagenPublicacion, form=PublicacionImagenForm, min_num=1,max_num=3, extra=3)

    def get(self, request, *args, **kwargs):
        form = PublicacionForm()
        form_descuento=DescuentoForm()
        form_imagenes=self.ImagenFormSet()
        return render(request, self.template_name, {'form': form, 'formset_imagen': form_imagenes, 'form_descuento':form_descuento})

    def post(self, request, *args, **kwargs):
        form = PublicacionForm(request.POST)
        form_descuento=DescuentoForm(request.POST)
        form_imagenes=self.ImagenFormSet(request.POST,request.FILES)
        if form.is_valid():
            if form_descuento.is_valid():
                if form_imagenes.is_valid():
                    publicacion=form.save()
                    descuento=form_descuento.save(commit=False)
                    descuento.servicio=publicacion.servicio
                    descuento.save()
                    imagenes=form_imagenes.save(commit=False)
                    for imagen in imagenes:
                        imagen.publicacion=publicacion
                        imagen.save()

        return render(request, self.template_name, {'form': form, 'formset_imagen': form_imagenes, 'form_descuento':form_descuento})

class EditarPromocion(TemplateView):
    template_name = "publicidad/administracion/crearEditar.html"

class PublicacionListView(ListView):
    model=Publicacion
    context_object_name = "publicaciones"
    template_name= "publicidad/administracion/lista.html"

#servicios
class ServicioDetailView(SingleObjectMixin, ListView):
    template_name = "servicios/detalle.html"
    paginate_by = 2
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Servicio.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicio'] = self.object
        return context

    def get_queryset(self):
        return self.object.descuentos.all()
        # return self.object.descuento_set.all()
