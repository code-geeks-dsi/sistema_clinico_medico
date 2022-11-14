#Python
from datetime import datetime
#Django
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView

#Propias
from ..models import Publicacion, ServicioMedico
from ..serializers import PublicacionSerializer, ServicioMedicoSerializer
##La url de esta pagina se invoca desde el archivo principal de url
class PaginaPrincipal(TemplateView):
    template_name = "publicidad/paginaPrincipal/paginaPrincipal.html"

def get_publicaciones(request):
    fecha=datetime.now().strftime("%Y-%m-%d")
    publicaciones=Publicacion.objects.filter(validez_fecha_fin__gte=fecha)
    publicaciones=PublicacionSerializer(publicaciones, many=True)
    return JsonResponse({"data":publicaciones.data})

def get_servicios_medicos(request):
    servicios=ServicioMedico.objects.all()
    servicios=ServicioMedicoSerializer(servicios, many=True)
    return JsonResponse({"data":servicios.data})