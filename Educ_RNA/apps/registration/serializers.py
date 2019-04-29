from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import (
    FieldDoesNotExist, ImproperlyConfigured, ValidationError,
)
from rest_framework.authtoken.models import Token

# Serializers del modulo de registro, que permiten mapear las instancias de los Modelos en formato JSON, para su envio
# a traves de los metodos


# Serializador para mapear el modelo Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    # Funcion para crear un usuario en la base de datos
    def create(self, validated_data):
        errors = []
        # Se obtienen los datos recibidos
        username = validated_data['username']
        password = validated_data['password']
        confirm_password = validated_data['confirm_password']
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        try:
            # Se realizan las validaciones de la contraseña
            validate_password(password, username)
            # Si la contraseña es valida, se verifica que la contraseña de confirmacion sea igual a ella
            if password == confirm_password:
                # Si las contraseñas coinciden se crea el usuario
                user = User.objects.create(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                # Hash de la contraseña
                user.set_password(password)
                user.save()
                return user
            # Si las contraseñas no coinciden se envia el mensaje de error correspondiente
            else:
                error = {'username': ["Claves no coinciden"]}
                return error
        # Si las validaciones de la contraseña no son exitosas, se detecta la excepcion y se envia el mensaje de error
        except ValidationError as error:
            pass_error = {'username':  error.__str__()}
            return pass_error

    # Clase Meta para mapear los campos del serializador con los campos del modelo
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'confirm_password', 'email')
