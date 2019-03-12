from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import (
    FieldDoesNotExist, ImproperlyConfigured, ValidationError,
)
from rest_framework.authtoken.models import Token

# Serializers del modulo de registro, que permiten mapear las instancias de los Modelos en formato JSON, para su envio
# a traves de los metodos


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def create(self, validated_data):
        errors = []
        username = validated_data['username']
        password = validated_data['password']
        confirm_password = validated_data['confirm_password']
        try:
            validate_password(password, username)
            if password == confirm_password:
                user = User.objects.create(
                    username=username,
                    email=validated_data['email'],
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name']
                )
                user.set_password(password)
                user.save()
            # token = Token.objects.create(user=user)
                return user
            else:
                error = {'username': "[Claves no coinciden]"}
                print(error)
                return error
        except ValidationError as error:
            passerror = {'username':  error.__str__()}
            return passerror


    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'confirm_password', 'email')



