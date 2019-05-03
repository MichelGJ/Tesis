from django.db import models

# Create your models here.
# Modelos para el modulo de lecciones


class Leccion(models.Model):
    nombre = models.CharField(max_length=120)


class Tema(models.Model):
    nombre = models.CharField(max_length=120)
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE)


class InfoTema(models.Model):
    presentacion = models.BooleanField(default=True)
    podcast = models.BooleanField(default=True)
    codigo = models.BooleanField(default=True)
    tema = models.OneToOneField(Tema, on_delete=models.CASCADE, null=True)


class Link(models.Model):
    presentacion = models.CharField(max_length=1024, null=True)
    presentaciond = models.CharField(max_length=1024, null=True)
    podcast = models.CharField(max_length=1024, null=True)
    codigo = models.CharField(max_length=1024, null=True)
    tema = models.OneToOneField(Tema, on_delete=models.CASCADE, null=True, unique=True)
