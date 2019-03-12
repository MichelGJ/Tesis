from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import ver_lecciones

urlpatterns = [
    path('ver/', login_required(ver_lecciones), name='ver'),
]
