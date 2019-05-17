from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import LogicaLecciones
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('ver/', login_required(LogicaLecciones.ver_lecciones), name='ver'),
    path('ver-temas/?id=<leccion_id>', login_required(LogicaLecciones.ver_temas), name="vertema"),
    path('presentacion/?id=<tema_id>', login_required(LogicaLecciones.presentacion), name="presentacion"),
    path('descargapres/?id=<tema_id>', login_required(LogicaLecciones.descargapresentacion), name="descargapres"),
    path('podcast/?id=<tema_id>', login_required(LogicaLecciones.podcast), name="podcast"),
    path('descargapod/?id=<tema_id>', login_required(LogicaLecciones.descargapodcast), name="descargapod"),
    path('error/', login_required(LogicaLecciones.error), name="error")
]

urlpatterns = format_suffix_patterns(urlpatterns)
