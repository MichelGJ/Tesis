from rest_framework import serializers
from .models import Leccion, Tema, InfoTema, Link, Quiz, Pregunta, Prueba, Respuesta, Progreso, Calificacion, Curso
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.db import IntegrityError


# Serializers del modulo de lecciones, que permiten mapear las instancias de los Modelos en formato JSON, para su envio
# a traves de los metodos
class LeccionesSerializer:

    # Serializador para mapear el modelo Leccion
    class CursoSerializer(serializers.ModelSerializer):
        # Clase Meta para mapear los campos del serializador con los campos del modelo
        class Meta:
            model = Curso
            fields = ('id', 'nombre')

    # Serializador para mapear el modelo Leccion
    class LeccionSerializer(serializers.ModelSerializer):

        # Clase Meta para mapear los campos del serializador con los campos del modelo
        class Meta:
            model = Leccion
            fields = ('id', 'nombre', 'curso_id')

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

    class PodcastSerializer(serializers.ModelSerializer):

        class Meta:
            model = Link
            fields = ('podcast',)

    class CodigoSerializer(serializers.ModelSerializer):

        class Meta:
            model = Link
            fields = ('codigo', 'repocodigo')


# Serializers del modulo de evaluaciones, que permiten mapear las instancias de los Modelos en formato JSON,
# para su envio a traves de los metodos
class EvaluacionesSerializer:

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
            fields = ('id', 'leccion_id')

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


# Serializers del modulo de registro, que permiten mapear las instancias de los Modelos en formato JSON, para su envio
# a traves de los metodos
class RegistrationSerializer:

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
                pass_error = {'username': error.__str__()}
                return pass_error

        # Clase Meta para mapear los campos del serializador con los campos del modelo
        class Meta:
            model = User
            fields = ('first_name', 'last_name', 'username', 'password', 'confirm_password', 'email')


# Serializers del modulo de usuarios, que permiten mapear las instancias de los Modelos en formato JSON, para su envio
# a traves de los metodos
class UsuariosSerializer:
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

    # Serializador para mapear el modelo Progreso
    class ProgresoSerializer(serializers.ModelSerializer):
        usuario_id = serializers.IntegerField(required=True)
        curso_id = serializers.IntegerField(required=True)
        tema_id = serializers.IntegerField(required=True)

        class Meta:
            model = Progreso
            fields = ('id', 'usuario_id', 'curso_id', 'tema_id')

    class CalificacionSerializer(serializers.ModelSerializer):
        usuario_id = serializers.IntegerField(required=True)
        prueba_id = serializers.IntegerField(required=True)

        class Meta:
            model = Calificacion
            fields = ('id', 'usuario_id', 'prueba_id', 'nota', 'mejor_nota', 'intentos')

