from django.contrib import admin
from modulo_expediente.models import Paciente, Expediente, ContieneConsulta
# Register your models here.
admin.site.register(Paciente)
admin.site.register(Expediente)
admin.site.register(ContieneConsulta)