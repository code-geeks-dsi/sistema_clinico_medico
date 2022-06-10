from django.urls import re_path
from . import consumers

websocket_urlpatterns=[
        re_path(r'ws/laboratorio/cola/',consumers.ColaLaboratorioConsumer.as_asgi())
]