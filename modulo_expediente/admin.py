from django.contrib import admin
from modulo_expediente.models import Consulta, Paciente, Expediente, ContieneConsulta, SignosVitales
# Register your models here.
admin.site.register(Paciente)
admin.site.register(Expediente)
admin.site.register(ContieneConsulta)
admin.site.register(Consulta)
admin.site.register(SignosVitales)