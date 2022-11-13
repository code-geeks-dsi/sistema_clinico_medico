#Python

#Django
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.shortcuts import get_object_or_404
from django.shortcuts import (render,redirect)
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist

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
        form_imagenes=self.ImagenFormSet(queryset=ImagenPublicacion.objects.none())
        return render(
            request, 
            self.template_name, 
            {
                'form': form, 
                'formset_imagen': form_imagenes, 
                'form_descuento':form_descuento, 
                'servicio': self.kwargs['servicio'], 
                'id_servicio': self.kwargs['id_servicio']
                })

    def post(self, request, *args, **kwargs):
        servicio = get_object_or_404(Servicio, id_servicio=self.kwargs['id_servicio'])
        form = PublicacionForm(request.POST)
        form_descuento=DescuentoForm(request.POST)
        form_imagenes=self.ImagenFormSet(request.POST, request.FILES)
        if form.is_valid():
            publicacion=form.save(commit=False)
            publicacion.servicio=servicio
            publicacion.save()
            if request.session.get('mensajes') is None:
                request.session['mensajes']=[]
            request.session['mensajes'].append({
                    'type':'success',
                    'data':'Promoción Guardada.'
                    })
            if form_descuento['habilitarDescuento'].value() == True:
                if form_descuento.is_valid():
                        descuento=form_descuento.save(commit=False)
                        descuento.publicacion=publicacion
                        descuento.save()
                        if request.session.get('mensajes') is None:
                            request.session['mensajes']=[]
                        request.session['mensajes'].append({
                        'type':'success',
                        'data':'Descuento Guardado.'
                        })

            if form_imagenes.is_valid():
                imagenes=form_imagenes.save(commit=False)
                for imagen in imagenes:
                    imagen.publicacion=publicacion
                    imagen.save()
                    request.session['mensajes'].append({
                    'type':'success',
                    'data':'Imagenes Guardadas.'
                    })
                return redirect('editar_publicacion',self.kwargs['servicio'], servicio.id_servicio,publicacion.id_publicacion)        

        return render(request, self.template_name, {'form': form, 'formset_imagen': form_imagenes, 'form_descuento':form_descuento})

# Publicaciones
class EditarPromocion(View):
    template_name = "publicidad/administracion/crearEditar.html"
    ImagenFormSet = modelformset_factory(ImagenPublicacion, form=PublicacionImagenForm, min_num=1,max_num=3, extra=3)

    def get(self, request, *args, **kwargs):
        publicacion=get_object_or_404(Publicacion, id_publicacion=self.kwargs['id_promocion'])
        try:
            descuento=Descuento.objects.get(publicacion=publicacion)
        except Descuento.DoesNotExist:
            descuento=None
        imagenes=publicacion.imagenes.all()
        form = PublicacionForm(instance=publicacion)
        if descuento is not None:
            form_descuento=DescuentoForm(instance=descuento, initial={'habilitarDescuento': True})
        else:
            form_descuento=DescuentoForm(initial={'habilitarDescuento': False})
        if imagenes is not None:
            form_imagenes=self.ImagenFormSet(queryset=imagenes,initial=[{publicacion:publicacion}])
        else:
            form_imagenes=self.ImagenFormSet(initial=[{publicacion:publicacion}])
        # recuperando mensajes para mostrarlos y limpiarlos
        mensajes=request.session.get('mensajes', [])
        if request.session.get('mensajes') is not None:
            del request.session['mensajes']
        return render(request, self.template_name, {
            'form': form, 
            'formset_imagen': form_imagenes, 
            'form_descuento':form_descuento, 
            'servicio':self.kwargs['servicio'],
            'id_servicio': self.kwargs['id_servicio'],
            'mensajes':mensajes
            })

    def post(self, request, *args, **kwargs):
        servicio = get_object_or_404(Servicio, id_servicio=self.kwargs['id_servicio'])
        publicacion=get_object_or_404(Publicacion, id_publicacion=self.kwargs['id_promocion'])
        try:
            descuento=Descuento.objects.get(publicacion=publicacion)
            form_descuento=DescuentoForm(request.POST, instance=descuento)
        except Descuento.DoesNotExist:
            descuento=None
            form_descuento=DescuentoForm(request.POST)
        imagenes=publicacion.imagenes.all()
        form = PublicacionForm(request.POST, instance=publicacion)
        if imagenes is not None:
            form_imagenes=self.ImagenFormSet(request.POST, request.FILES, queryset=imagenes)
        else:
            form_imagenes=self.ImagenFormSet(request.POST, request.FILES)

        if form.is_valid():
            publicacion=form.save(commit=False)
            publicacion.servicio=servicio
            publicacion.save()
            if form_descuento['habilitarDescuento'].value() == True:
                if form_descuento.is_valid():
                        descuento=form_descuento.save(commit=False)
                        descuento.publicacion=publicacion
                        descuento.save()
                        if request.session.get('mensajes') is None:
                            request.session['mensajes']=[]
                        request.session['mensajes'].append({
                        'type':'success',
                        'data':'Descuento Guardado.'
                        })
            elif descuento is not None:
                descuento.delete()

            if form_imagenes.is_valid():
                imagenes=form_imagenes.save(commit=False)
                for imagen in imagenes:
                    imagen.publicacion=publicacion
                    imagen.save()
                    if request.session.get('mensajes') is None:
                        request.session['mensajes']=[]
                    request.session['mensajes'].append({
                    'type':'success',
                    'data':'Imagenes Guardadas.'
                    })

            else:
                print(form_imagenes.non_form_errors())
                print(form_imagenes.errors)
            return redirect('editar_publicacion',self.kwargs['servicio'],servicio.id_servicio,publicacion.id_publicacion)
        return render(request, self.template_name, {'form': form, 'formset_imagen': form_imagenes, 'form_descuento':form_descuento})

class EliminarPromocionView(DeleteView):
    model = Publicacion
    template_name= "publicidad/administracion/confirmar_eliminar.html"
    def get_success_url(self):
        return reverse_lazy('ver_publicaciones',kwargs={'id_servicio':self.kwargs['id_servicio'],'servicio':self.kwargs['servicio']})

class PublicacionListView(ListView):
    model=Publicacion
    paginate_by = 10
    context_object_name = "publicaciones"
    template_name= "publicidad/administracion/lista.html"
    
    def get_queryset(self):
        self.servicio = get_object_or_404(Servicio, id_servicio=self.kwargs['id_servicio'])
        return Publicacion.objects.filter(servicio=self.servicio)

#servicios
# class ServicioDetailView(SingleObjectMixin, ListView):
#     template_name = "servicios/detalle.html"
#     paginate_by = 2
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object(queryset=Servicio.objects.all())
#         return super().get(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['servicio'] = self.object
#         return context

#     def get_queryset(self):
#         return self.object.descuentos.all()

