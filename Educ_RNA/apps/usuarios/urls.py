from django.urls import path
from apps.usuarios.views import index,login

urlpatterns = [
    path('', login, name='login'),
    path('index/', index, name='index'),
]
