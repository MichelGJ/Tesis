from django.contrib.auth import authenticate
from django.http import JsonResponse
from apps.lecciones.serializers import LeccionSerializer, TemaSerializer, InfoTemaSerializer, PresentacionesSerializer,\
                                        PodcastSerializer
from apps.evaluaciones.serializers import QuizSerializer, PreguntaSerializer, RespuestaSerializer, PruebaSerializer
from apps.registration.serializers import UsuarioSerializer
from apps.usuarios.serializers import PasswordChangeSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView
from apps.usuarios.serializers import ModificarUsuarioSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.exceptions import ValidationError
# Vistas del API, en este caso se trata de la logica y las llamadas a las funciones necesarias


# Funcion que recibe las creedenciales de un usuario y determina si esta registrado
@method_decorator(csrf_exempt)
def login(request):
    # Obtiene las creedenciales que se le envian en la llamada
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    # Autentica si existe el usuario y si la contraseña corresponde al mismo usuario
    user = authenticate(username=username, password=password)
    # En caso de que la autenticacion sea exitosa se envia el usuario y el codigo 200(success)
    if user is not None:
        data = {'user': str(user)}
        return JsonResponse(data, status=200)
    # En caso de fallar la autenticacion se envia el codigo 404(not found)
    else:
        return HttpResponse(status=404)


# Metodo que registra el usuario en la base de datos
class RegistrarUsuario(CreateAPIView):
    serializer_class = UsuarioSerializer


# Metodo que actualiza informacion del usuario en la base de datos
class ActualizarUsuario(UpdateAPIView):
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = ModificarUsuarioSerializer


# Metodo que realiza el cambio de contraseñaa de un usuario
class CambioContrasena(UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    model = User

    # Funcion que recibe los datos necesarios, y realiza el cambio de contraseña si todos los requerimientos se cumplen
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # Si el serializador es valido se extraen los datos que contiene
        if serializer.is_valid():
            username = serializer.data.get("username")
            password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")
            new_password2 = serializer.data.get("new_password2")
            # Se autentica el usuario para verificar si la contraseña actual es la correcta
            user = authenticate(username=username, password=password)
            # Si el usuario no coincide con la clave se responde con un mensaje de error
            if not user:
                return Response({"old_password": ["Clave actual incorrecta"]}, status=status.HTTP_400_BAD_REQUEST)
            # Si el usuario coincide se revisa que la contraseña de confirmacion sea igual a la nueva introducida
            if new_password == new_password2:
                # Si la contraseña de confirmacion es igual a la nueva se hashea y almacena la contraseña nueva,
                # y se responde con un mensaje de exito
                user.set_password(new_password)
                user.save()
                return Response("Success.", status=status.HTTP_200_OK)
            else:
                # Si la contraseña de confirmacion no es igual a la nueva se envia el mensaje de error correspondiente
                return Response({"new_password": ["Claves no coinciden"]}, status=status.HTTP_400_BAD_REQUEST)
        # Si el serializador no es valido se envia el mensaje de error correspondiete
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Metodo que obtiene de la base de datos la lista completa de lecciones
class VerLecciones(ListAPIView):
    serializer_class = LeccionSerializer
    queryset = serializer_class.Meta.model.objects.all()


# Metodo que obtiene la lista de temas de una leccion determinada, dado su id
class VerTemas(ListAPIView):
    serializer_class = TemaSerializer
    model = serializer_class.Meta.model
    paginate_by = 100

    # Funcion que busca con el id dado la lista de temas correspondiente
    def get_queryset(self):
        leccion_id = self.kwargs['leccion_id']
        queryset = self.model.objects.filter(leccion_id=leccion_id)
        return queryset.order_by('id')


# Metodo que obtiene la info un tema determinado, dado su id
class VerInfoTema(RetrieveAPIView):
    serializer_class = InfoTemaSerializer
    lookup_field = "tema_id"
    queryset = serializer_class.Meta.model.objects.all()


# Metodo que obtiene los links de las presentaciones de un tema determinado, dado su id
class VerLinksPresentaciones(RetrieveAPIView):
    serializer_class = PresentacionesSerializer
    lookup_field = "tema_id"
    queryset = serializer_class.Meta.model.objects.all()


# Metodo que obtiene el link del podcast de un tema determinado, dado su id
class VerLinkPodcast(RetrieveAPIView):
    serializer_class = PodcastSerializer
    lookup_field = "tema_id"
    queryset = serializer_class.Meta.model.objects.all()


# Metodo que obtiene el quiz de un tema dado su id
class GetQuiz(RetrieveAPIView):
    serializer_class = QuizSerializer
    lookup_field = "tema_id"
    queryset = serializer_class.Meta.model.objects.all()


# Metodo que obtiene la prueba de una leccion dado su id
class GetPrueba(RetrieveAPIView):
    serializer_class = PruebaSerializer
    lookup_field = "leccion_id"
    queryset = serializer_class.Meta.model.objects.all()


# Metodo que obtiene la lista de preguntas de un quiz dado su id
class GetPreguntaQuiz(ListAPIView):
    serializer_class = PreguntaSerializer
    model = serializer_class.Meta.model
    queryset = serializer_class.Meta.model.objects.all()

    # Funcion que busca con el id del quiz la lista de preguntas correspondiente
    def get_queryset(self):
        quiz_id = self.kwargs['quiz_id']
        queryset = self.model.objects.filter(quiz_id=quiz_id)
        return queryset.order_by('id')


# Metodo que obtiene la lista de preguntas de una prueba dado su id
class GetPreguntaPrueba(ListAPIView):
    serializer_class = PreguntaSerializer
    model = serializer_class.Meta.model
    queryset = serializer_class.Meta.model.objects.all()

    # Funcion que busca con el id del quiz la lista de preguntas correspondiente
    def get_queryset(self):
        prueba_id = self.kwargs['prueba_id']
        queryset = self.model.objects.filter(prueba_id=prueba_id)
        return queryset.order_by('id')


# Metodo que consulta una pregunta por su propio id
class GetPreguntaId(RetrieveAPIView):
    serializer_class = PreguntaSerializer
    lookup_field = "id"
    queryset = serializer_class.Meta.model.objects.all()


# Metodo que obtiene la lista de respuestas de una pregunta dado su id
class GetRespuesta(ListAPIView):
    serializer_class = RespuestaSerializer
    model = serializer_class.Meta.model
    queryset = serializer_class.Meta.model.objects.all()

    # Funcion que busca con el id del quiz la lista de preguntas correspondiente
    def get_queryset(self):
        pregunta_id = self.kwargs['pregunta_id']
        queryset = self.model.objects.filter(pregunta_id=pregunta_id)
        return queryset.order_by('id')


# Metodo que consulta una respuesta por su propio id
class GetRespuestaId(RetrieveAPIView):
    serializer_class = RespuestaSerializer
    lookup_field = "id"
    queryset = serializer_class.Meta.model.objects.all()
