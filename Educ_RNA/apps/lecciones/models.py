from django.db import models


# Create your models here.
class Leccion(models.Model):
    nombre = models.CharField(max_length=120)


class Tema(models.Model):
    nombre = models.CharField(max_length=120)
    id_leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE)


class InfoTema(models.Model):
    orden = models.IntegerField()
    contenido = models.CharField(max_length=1024)
    id_tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
