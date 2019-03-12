from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from apps.lecciones.serializers import LeccionSerializer, TemaSerializer
from apps.registration.serializers import UsuarioSerializer
from apps.usuarios.serializers import PasswordChangeSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from apps.lecciones.models import Leccion, Tema
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView
from apps.usuarios.serializers import ModificarUsuarioSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.views import auth_login

# Vistas del API, en este caso se trata de la logica y las llamadas a las funciones necesarias


# Funcion que recibe las creedenciales de un usuario y determina si esta registrado.
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


# Funcion que registra el usuario en la base de datos.
class RegistrarUsuario(CreateAPIView):
    serializer_class = UsuarioSerializer


class ActualizarUsuario(UpdateAPIView):
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = ModificarUsuarioSerializer


@api_view(['GET'])
def ver_lecciones(request):
    queryset = Leccion.objects.all().values('nombre')
    serializer = LeccionSerializer(queryset, many=True)
    return Response(serializer.data)


class VerLecciones(ListAPIView):
    queryset = Leccion.objects.all().values('nombre')
    serializer_class = LeccionSerializer


class VerLeccion(RetrieveAPIView):
    lookup_field = 'id'
    queryset = Leccion.objects.all()
    serializer_class = LeccionSerializer


class VerTemas(ListAPIView):
    serializer_class = TemaSerializer
    model = serializer_class.Meta.model
    paginate_by = 100

    def get_queryset(self):
        leccion_id = self.kwargs['leccion_id']
        queryset = self.model.objects.filter(leccion_id=leccion_id)
        return queryset.order_by('id')


class CambioContrasena(UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            username = serializer.data.get("username")
            password = serializer.data.get("old_password")
            newpassword = serializer.data.get("new_password")
            newpassword2 = serializer.data.get("new_password2")
            user = authenticate(username=username, password=password)
            # Check old password
            if not user:
                return Response({"old_password": ["Clave actual incorrecta"]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            if newpassword == newpassword2:
                user.set_password(newpassword)
                user.save()
                return Response("Success.", status=status.HTTP_200_OK)
            else:
                return Response({"new_password": ["Claves no coinciden."]}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
