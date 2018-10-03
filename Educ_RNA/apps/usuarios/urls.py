from django.urls import path
from apps.usuarios.views import index

urlpatterns = [
    path('', index, name='index'),
]
