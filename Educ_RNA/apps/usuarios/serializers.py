from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
# Serializers del modulo de usuarios, que permiten mapear las instancias de los Modelos en formato JSON, para su envio
# a traves de los metodos


# Serializador para la modificacion del usuario
class ModificarUsuarioSerializer(serializers.ModelSerializer):

    # Clase Meta para mapear los campos del serializador con los campos del modelo
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


# Serializador para el cambio de contraseña del usuario
class PasswordChangeSerializer(serializers.Serializer):

    username = serializers.CharField()
    old_password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password2 = serializers.CharField(required=True, style={'input_type': 'password'})

    # Funcion que realiza todas las validaciones de la contraseña
    def validate_new_password(self, value):
        validate_password(value)
        return value
