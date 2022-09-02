from django.shortcuts import render
from modulo_expediente.serializers import ControlSubsecuenteConsultaSerializer
from modulo_expediente.models import ( ContieneConsulta, SignosVitales)
from django.http import JsonResponse
from django.views.generic import View

class ControlSubsecuenteView(View): 
        template_name = "expediente/consulta/control_subsecuente.html"

        def get(self, request, *args, **kwargs):

            id_consulta=int(self.kwargs['id_consulta']) 
            contiene_consulta=ContieneConsulta.objects.filter(consulta__id_consulta=id_consulta).first()
            expediente=contiene_consulta.expediente_id
            contiene_consulta=ContieneConsulta.objects.filter(expediente_id=expediente).exclude(consulta__id_consulta=id_consulta).select_related('consulta')
            lista=[]
            for i in range(len(contiene_consulta)):
                
                c={
                     'id_consulta':"",
                     'fecha':"",
                     'diagnostico':"",
                }
                c['id_consulta']=contiene_consulta[i].consulta.id_consulta
                c['fecha']=contiene_consulta[i].consulta.fecha
                c['diagnostico']=contiene_consulta[i].consulta.diagnostico
            
                lista.append(c)
            
            return render(request,self.template_name,{'consultas':lista, 'id_consulta':id_consulta})
           
class ControlSubsecuenteConsultaView(View): 
    def get(self, request, *args, **kwargs):
        id_consulta=int(self.kwargs['id_consulta']) 
        signos_vitales_data=SignosVitales.objects.filter(consulta_id=id_consulta).order_by('-fecha').first()
        signos_vitales=ControlSubsecuenteConsultaSerializer(signos_vitales_data,many=False)
        return JsonResponse({'signos_vitales':signos_vitales.data})
        


