from django.urls import path
from apps.usuarios.views import index,perfil
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('index/', login_required(index), name='index'),
    path('perfil/', login_required(perfil), name='perfil'),
]
