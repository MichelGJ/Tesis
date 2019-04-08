from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import ver_lecciones, ver_temas, presentacion, descarga
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('ver/', login_required(ver_lecciones), name='ver'),
    path('ver-temas/?id=<leccion_id>', login_required(ver_temas), name="vertema"),
    path('presentacion/?id=<tema_id>', login_required(presentacion), name="presentacion"),
    path('descarga/<nombre>', login_required(descarga), name="descarga"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
