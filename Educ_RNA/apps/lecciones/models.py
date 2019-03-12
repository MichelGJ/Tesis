from django.db import models

# Create your models here.
# Modelos para el modulo de lecciones


class Leccion(models.Model):
    nombre = models.CharField(max_length=120)


class Tema(models.Model):
    nombre = models.CharField(max_length=120)
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE)


class InfoTema(models.Model):
    orden = models.IntegerField()
    contenido = models.CharField(max_length=1024)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
