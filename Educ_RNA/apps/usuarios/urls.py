from django.urls import path
from apps.usuarios.views import index
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('index/', login_required(index), name='index'),

]
