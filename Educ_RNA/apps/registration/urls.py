from django.urls import path
from apps.registration.views import login, RegistroUsuario, password
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', login_required(login), name='plogin'),
    path('registrar/', RegistroUsuario.as_view(), name='registrar'),
    path('password/', password, name='registrar'),
]