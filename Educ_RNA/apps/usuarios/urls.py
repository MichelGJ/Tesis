from django.urls import path
from apps.usuarios.views import LogicaUsuarios
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('index/', login_required(LogicaUsuarios.index), name='index'),
    path('perfil/', login_required(LogicaUsuarios.perfil), name='perfil'),
    path('abrir-modificar/?id=<id>', login_required(LogicaUsuarios.AbrirModificarUsuario.as_view()), name='abrirmodificar'),
    path('modificar/', login_required(LogicaUsuarios.modificacion_usuario), name='modificar'),
    path('cambiar-contrasena/', login_required(LogicaUsuarios.cambio_constrasena), name='cambiar'),
    path('nosotros/', login_required(LogicaUsuarios.nosotros), name='nosotros'),
    path('progreso/', login_required(LogicaUsuarios.progreso), name='progreso'),
]
