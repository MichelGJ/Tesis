from rest_framework import serializers
from .models import Leccion, Tema, InfoTema, Link

# Serializers del modulo de lecciones, que permiten mapear las instancias de los Modelos en formato JSON, para su envio
# a traves de los metodos


# Serializador para mapear el modelo Leccion
class LeccionSerializer(serializers.ModelSerializer):

    # Clase Meta para mapear los campos del serializador con los campos del modelo
    class Meta:
        model = Leccion
        fields = ('id', 'nombre')


# Serializador para mapear el modelo Tema
class TemaSerializer(serializers.ModelSerializer):

    # Clase Meta para mapear los campos del serializador con los campos del modelo
    class Meta:
        model = Tema
        fields = ('id', 'nombre', 'leccion_id')


class InfoTemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = InfoTema
        fields = ('id', 'tema_id', 'presentacion', 'podcast', 'codigo')


class PresentacionesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Link
        fields = ('presentacion', 'presentaciond')
