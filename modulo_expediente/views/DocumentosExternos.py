#Python
import boto3
import environ
import pathlib 
import uuid
#Django
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView
#Propios
from ..forms import DocumentoExpedienteForm
from ..models import ContieneConsulta, DocumentoExpediente
from ..serializers import DocumentoExternoSerializer

##Para cargar las variables de entorno
env = environ.Env()
environ.Env.read_env()

#Clase para almacenamiento de archivos
##Para esta vista es necesario tener permiso de ver expedientes
class ExamenesExternosCreateView(PermissionRequiredMixin,TemplateView):
    template_name = "expediente/examenes_externos/almacenar_examenes_externos.html"
    permission_required = ('modulo_expediente.view_expediente')
    form_class = DocumentoExpedienteForm
    ##Cargar
    def get(self, request, *args, **kwargs):
        id_consulta=self.kwargs['id_consulta']
        expediente=ContieneConsulta.objects.filter(consulta__id_consulta=id_consulta).values('expediente','expediente__id_paciente__nombre_paciente').first()
        form = self.form_class()
        #Consultando Archivos
        if expediente!= None:
            archivos=DocumentoExpediente.objects.filter(expediente__id_expediente=expediente['expediente']).order_by('-fecha')
            return render(request, self.template_name, {'form': form, 'consulta': id_consulta, 'archivos':archivos, 'paciente':expediente['expediente__id_paciente__nombre_paciente']})
        else:
            raise Http404("Consulta no encontrada")
    ##Guardar Datos
    def post(self, request, *args, **kwargs):
        id_consulta=self.kwargs['id_consulta']
        expediente=ContieneConsulta.objects.filter(consulta__id_consulta=id_consulta).first().expediente
        #Recueperando Archivo
        archivo=request.FILES['file']
        nombre=archivo.name
        ##Generando nombre aleatorio
        file_extension = pathlib.Path(nombre).suffix 
        archivo.name=f'{str(uuid.uuid4())}{file_extension}'
        #Almacenando archivo
        documento=DocumentoExpediente.objects.create(
            titulo= nombre,
            documento=archivo,
            expediente=expediente,
            empleado=request.user
        )
        response={
                    'id':documento.id_documento,
                    'fecha':documento.fecha.strftime('%d de %b de %Y a las %I:%M '),
                    'propietario':f'{expediente.id_paciente.nombre_paciente} {expediente.id_paciente.apellido_paciente}'
                }
        return JsonResponse(response)
        #return HttpResponseServerError('PARA Errores')     

##Esto genera una url para accdeder al archivo surante 60 segundos
##Para acceder aquí es necesario estar logeado con el permiso para ver los expedientes
class DocumentosExternosURLview(PermissionRequiredMixin, View):
    permission_required = ('modulo_expediente.view_expediente')
    ##Genera una url con el token de acceso
    def get(self, request, *args, **kwargs):
        id_documento=self.kwargs['id_documento']
        try:
            documentos=DocumentoExpediente.objects.get(id_documento=id_documento)
            client = boto3.client('s3')
            response = client.generate_presigned_url('get_object',Params={'Bucket': 'code-geek-medic',
                                                                    'Key': f'static/{documentos.documento}'
                                                                    },
                                                ExpiresIn=1800) #tiempo en segundos
            return redirect(response)
        except ObjectDoesNotExist:
            raise Http404('Archivo no encontrado')

    ##Metodo para eliminar archivos
    def delete(self, request, *args, **kwargs):
        id_documento=self.kwargs['id_documento']
        try:
            documento=DocumentoExpediente.objects.get(id_documento=id_documento)
            client = boto3.resource('s3')
            client.Object(env('AWS_STORAGE_BUCKET_NAME'), f'static/{documento.documento}').delete()
            
            documento.delete()
            ##Recuperando elementos para actualizar lista
            archivos=DocumentoExpediente.objects.filter(expediente=documento.expediente).order_by('-fecha')
            archivos=DocumentoExternoSerializer(archivos, many=True)

            response={
                        'type':'success',
                        'data':'Archivo Eliminado',
                        'archivos':archivos.data,
                    }
        except ObjectDoesNotExist:
            response={
                'type':'warning',
                'data':'Archivo no encontrado.'
            }
            
        return JsonResponse(response)

##Generador de urls de descargas
class DocumentosExternosURLDownload(PermissionRequiredMixin, View):
    permission_required = ('modulo_expediente.view_expediente')
    ##Genera una url con el token de acceso
    def get(self, request, *args, **kwargs):
        id_documento=self.kwargs['id_documento']
        try:
            documentos=DocumentoExpediente.objects.get(id_documento=id_documento)
            client = boto3.client('s3')
            response = client.generate_presigned_url('get_object',Params={'Bucket': 'code-geek-medic',
                                                                    'Key': f'static/{documentos.documento}',
                                                                    'ResponseContentEncoding':'binary',
                                                                    'ResponseContentDisposition':f'attachment; filename= {documentos.titulo}',
                                                                    },
                                                ExpiresIn=600) #10 minutos para descargar
            return redirect(response)
        except ObjectDoesNotExist:
            raise Http404('Archivo no encontrado')
