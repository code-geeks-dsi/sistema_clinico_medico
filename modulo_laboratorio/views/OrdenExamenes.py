#Django
from django.urls import reverse
from django.views.generic import  TemplateView
from django.shortcuts import redirect
##Libreria Propias
from modulo_laboratorio.models import ( EsperaExamen)
from modulo_laboratorio.views.Resultado import sync_cola

class OrdenExamenCreate(TemplateView):
    
    #Imprimir en pantalla el formulario de creación de orden
    def get(self, request, *args, **kwargs):
        ##Creando Orden
        id_paciente=int(self.kwargs['id_paciente'])
        orden=EsperaExamen.create(
            id_paciente=id_paciente
        )
        orden.save()
        sync_cola()
        return redirect(reverse('update_orden_examenes',
                            kwargs={'id_paciente':id_paciente,'id_orden':orden.id},))


