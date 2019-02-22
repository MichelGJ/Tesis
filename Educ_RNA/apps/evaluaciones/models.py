from django.db import models
from apps.lecciones.models import Leccion, Tema


# Create your models here.
class Prueba(models.Model):
    nombre = models.CharField(max_length=120)
    modelo = models.IntegerField()
    id_leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE)


class Quiz(models.Model):
    id_tema = models.ForeignKey(Leccion, on_delete=models.CASCADE)


class Pregunta(models.Model):
    contenido = models.CharField(max_length=120)
    id_prueba = models.ForeignKey(Prueba, on_delete=models.CASCADE, null=True)
    id_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)


class Respuesta(models.Model):
    contenido = models.CharField(max_length=120)
    id_pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, null=True)
