from django.db import models
from apps.lecciones.models import Leccion, Tema

# Create your models here
# Modelos para el modulo de evaluaciones


class Prueba(models.Model):
    nombre = models.CharField(max_length=120)
    modelo = models.IntegerField()
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE)


class Quiz(models.Model):
    tema = models.ForeignKey(Leccion, on_delete=models.CASCADE)


class Pregunta(models.Model):
    contenido = models.CharField(max_length=120)
    prueba = models.ForeignKey(Prueba, on_delete=models.CASCADE, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)


class Respuesta(models.Model):
    contenido = models.CharField(max_length=120)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, null=True)
    respuestacorrecta = models.BooleanField()
