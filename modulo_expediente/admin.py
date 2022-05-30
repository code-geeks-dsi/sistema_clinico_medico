from django.contrib import admin
from modulo_control.models import Empleado,Rol
from modulo_expediente.models import Consulta, Paciente, Expediente, ContieneConsulta, SignosVitales, Medicamento
# Register your models here.
admin.site.register(Paciente)
admin.site.register(Expediente)
admin.site.register(ContieneConsulta)
admin.site.register(Consulta)
admin.site.register(SignosVitales)
admin.site.register(Rol)
admin.site.register(Medicamento)
