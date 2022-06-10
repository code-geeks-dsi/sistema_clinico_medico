"""
ASGI config for sistema_clinico_medico project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.urls import path,include
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
import modulo_expediente.routing
import modulo_laboratorio.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_clinico_medico.settings')

application = ProtocolTypeRouter({
        'http':get_asgi_application(),
        'websocket':AuthMiddlewareStack(
                URLRouter(
                        modulo_laboratorio.routing.websocket_urlpatterns,
                        modulo_expediente.routing.websocket_urlpatterns
                )
        )
})

