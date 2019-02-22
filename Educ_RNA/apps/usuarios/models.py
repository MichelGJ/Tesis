from django.db import models
from django.contrib.auth.models import User
from apps.lecciones.models import Tema
from apps.evaluaciones.models import Prueba


# Create your models here.
class Calificacion(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_prueba = models.ForeignKey(Prueba, on_delete=models.CASCADE)
    nota = models.CharField(max_length=2)
    mejor_nota = models.CharField(max_length=2)
    intentos = models.IntegerField()

    class Meta:
        unique_together = ("id_usuario", "id_prueba")


class Progreso(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_tema = models.ForeignKey(Tema, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("id_usuario", "id_tema")


