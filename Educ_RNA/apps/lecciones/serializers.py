from rest_framework import serializers
from .models import Leccion, Tema

# Serializers del modulo de lecciones, que permiten mapear las instancias de los Modelos en formato JSON, para su envio
# a traves de los metodos


class LeccionSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Leccion
        fields = ('id', 'nombre')


class TemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tema
        fields = ('id', 'nombre', 'leccion_id')

