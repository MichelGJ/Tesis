from django.db import models
from django.contrib.auth.models import User
from apps.lecciones.models import Tema
from apps.evaluaciones.models import Prueba

# Create your models here.
# Modelos para el modulo de usuarios


class Calificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    prueba = models.ForeignKey(Prueba, on_delete=models.CASCADE)
    nota = models.CharField(max_length=2)
    mejor_nota = models.CharField(max_length=2)
    intentos = models.IntegerField()

    class Meta:
        unique_together = ("usuario", "prueba")


class Progreso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("usuario", "tema")


