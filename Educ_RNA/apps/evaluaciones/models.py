from django.db import models
from apps.lecciones.models import Leccion, Tema

# Entidades del modulo evaluaciones


class Prueba(models.Model):
    leccion = models.OneToOneField(Leccion, on_delete=models.CASCADE)

    class Meta:
        managed = False


class Quiz(models.Model):
    tema = models.OneToOneField(Tema, on_delete=models.CASCADE, null=True)

    class Meta:
        managed = False


class Pregunta(models.Model):
    contenido = models.CharField(max_length=150, unique=True)
    prueba = models.ForeignKey(Prueba, on_delete=models.CASCADE, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)

    class Meta:
        managed = False


class Respuesta(models.Model):
    contenido = models.CharField(max_length=320)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, null=True)
    correcta = models.BooleanField()

    class Meta:
        managed = False
