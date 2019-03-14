from django.urls import path
from apps.usuarios.views import index, perfil, AbrirModificarUsuario, modificacion_usuario, cambio_constrasena, nosotros\
    , progreso
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('index/', login_required(index), name='index'),
    path('perfil/', login_required(perfil), name='perfil'),
    path('abrir-modificar/?id=<id>', login_required(AbrirModificarUsuario.as_view()), name='abrirmodificar'),
    path('modificar/', login_required(modificacion_usuario), name='modificar'),
    path('cambiar-contrasena/', login_required(cambio_constrasena), name='cambiar'),
    path('nosotros/', login_required(nosotros), name='nosotros'),
    path('progreso/', login_required(progreso), name='progreso'),
]
