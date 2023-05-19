from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'help text'

    def handle(self, *args, **options):
        hora_inicio=timedelta(hours=7, minutes=30)
        primer_paciente=timedelta(minutes=random.randint(0, 80))
        examenes_random=random.randint(2, 9)
        examenes_rutina=random.randint(1,4)
        print(f'El primer paciente llega a las {hora_inicio+primer_paciente}, se hacen {examenes_random} examenes y {examenes_rutina} examenes de rutina')
        hora_llegada=hora_inicio
    ####Consultas de la mañana
        pass