#Python
#Django
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils import timezone

#Librerias Propias
from ..models import Resultado
from ..serializers import ResultadoLaboratorioSerializer

#Clase para ver la bitacora
class BitacoraView(PermissionRequiredMixin,TemplateView):
    permission_required = ('modulo_laboratorio.change_resultado')
    template_name = "laboratorio/bitacora.html"
    login_url='/login/'  
    response={'type':'','data':'', 'info':''}

    def post(self, request, *args, **kwargs):
        fecha=timezone.now()
        resultados=Resultado.objects.filter(fecha_hora_toma_de_muestra__year=fecha.year
            ,fecha_hora_toma_de_muestra__month=fecha.month).select_related('orden_de_laboratorio__expediente__id_paciente').order_by('numero_cola_resultado')
        resultados=ResultadoLaboratorioSerializer(resultados,many=True)
        
        self.response['info']=resultados.data

        return JsonResponse(self.response)

