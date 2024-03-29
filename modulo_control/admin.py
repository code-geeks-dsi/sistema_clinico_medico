from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from modulo_control.models import Doctor, Empleado, Enfermera, LicLaboratorioClinico, Secretaria

class UserAdmin(BaseUserAdmin):
    list_display = ('email','es_staff')
    list_filter = ('es_staff',)
    fieldsets = ((None, 
                  {'fields':('email','password')}), 
                  ('Información Personal',{'fields':('nombres', 'apellidos','fechaNacimiento'
                  ,'fechaCreacion')}),
                  ('Permissions',{'fields':('es_staff','es_activo', 'es_superuser','groups', 'user_permissions')})
                  ,)
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}),)
    #form = CustomUserChangeForm
    #add_form = CustomUserCreationForm
    search_fields =('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(Empleado, UserAdmin)

admin.site.register(Enfermera)
admin.site.register(Doctor)
admin.site.register(Secretaria)
admin.site.register(LicLaboratorioClinico)
