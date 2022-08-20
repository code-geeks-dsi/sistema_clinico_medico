from modulo_expediente.models import ( Dosis, ContieneConsulta,
        RecetaMedica) 
from django.views.generic import View
from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string
import tempfile
from datetime import date
class RecetaMedicaPdfView(View):  
    def get(self, request, *args, **kwargs):
        id_consulta=int(self.kwargs['id_consulta'])
        #consultando datos del paciente
        contiene_consulta=ContieneConsulta.objects.get(consulta__id_consulta=id_consulta).latest('fecha_de_cola')
        paciente=contiene_consulta.expediente.id_paciente 
        fecha=date.today()
        #consultando datos de  la dosis  medicamento
        # receta=RecetaMedica.objects.filter(consulta_id=id_consulta).latest('fecha')
        receta=RecetaMedica.objects.filter(consulta_id=id_consulta).first()
        dosis=Dosis.objects.filter(receta_medica=receta.id_receta_medica)
        data={'paciente':paciente,'fecha':fecha,'dosis':dosis} 
        #generando pdf
        #puede recibir la info como diccionario
        html_string = render_to_string('recetaMedica.html',data)
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="recetaMedica.pdf"'
        response['Content-Transfer-Encoding'] = 'binary'
        #Crea un archivo temporal
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
        return response
