from django.urls import path
from apps.usuarios.views import index, prueba, home, login, RegistroUsuario
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('index/', login_required(index), name='index'),
    path('prueba/', login_required(prueba), name='prueba'),
    path('prueba/home', login_required(home), name='prueba'),
    path('login/', login_required(login), name='plogin'),
    path('registrar/', RegistroUsuario.as_view(), name='registrar')
]
