from rest_framework import serializers
from .models import Prueba, Quiz, Pregunta, Respuesta


# Serializador para mapear el modelo Quiz
class QuizSerializer(serializers.ModelSerializer):

    # Clase Meta para mapear los campos del serializador con los campos del modelo
    class Meta:
        model = Quiz
        fields = ('id',)


# Serializador para mapear el modelo Prueba
class PruebaSerializer(serializers.ModelSerializer):

    # Clase Meta para mapear los campos del serializador con los campos del modelo
    class Meta:
        model = Prueba
        fields = ('id',)


# Serializador para mapear el modelo Pregunta
class PreguntaSerializer(serializers.ModelSerializer):

    # Clase Meta para mapear los campos del serializador con los campos del modelo
    class Meta:
        model = Pregunta
        fields = ('id', 'contenido')


# Serializador para mapear el modelo Respuesta
class RespuestaSerializer(serializers.ModelSerializer):

    # Clase Meta para mapear los campos del serializador con los campos del modelo
    class Meta:
        model = Respuesta
        fields = ('id', 'contenido', 'correcta')
