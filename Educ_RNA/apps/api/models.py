from django.db import models
from django.contrib.auth.models import User

# Modelos para migrar a la base de datos


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


class Prueba(models.Model):
    leccion = models.OneToOneField(Leccion, on_delete=models.CASCADE)


class Quiz(models.Model):
    tema = models.OneToOneField(Tema, on_delete=models.CASCADE, null=True)


class Pregunta(models.Model):
    contenido = models.CharField(max_length=150, unique=True)
    prueba = models.ForeignKey(Prueba, on_delete=models.CASCADE, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)


class Respuesta(models.Model):
    contenido = models.CharField(max_length=320)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, null=True)
    correcta = models.BooleanField()


class Calificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='C_U_FK')
    prueba = models.ForeignKey(Prueba, on_delete=models.CASCADE, related_name='C_T_FK')
    nota = models.CharField(max_length=2)
    mejor_nota = models.CharField(max_length=2)
    intentos = models.IntegerField()

    class Meta:
        unique_together = ("usuario", "prueba")


class Progreso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='P_U_FK', unique=True)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name='P_T_FK')

    class Meta:
        unique_together = ("usuario", "tema")

