import git
from django.http import HttpResponse

def git_pull(request):
    if request.method == 'GET':
        try:
            # Ruta al directorio raíz de tu proyecto Django
            project_root = '/workspaces/sistema_clinico_medico'

            # Acceder al repositorio git en el directorio raíz
            repo = git.Repo(project_root)

            # Realizar el git pull
            repo.remotes.origin.pull()

            # Realizar acciones adicionales después del git pull
            # por ejemplo, actualización de dependencias o migraciones

            return HttpResponse('Git pull successful')
        except Exception as e:
            return HttpResponse(f'Error during git pull: {str(e)}', status=500)

    return HttpResponse('Invalid request method', status=400)
