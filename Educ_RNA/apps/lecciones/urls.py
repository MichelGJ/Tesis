from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import LogicaLecciones
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('ver/', login_required(LogicaLecciones.ver_cursos), name='ver'),
    path('ver-lecciones/(?P<curso_id>\d+)', login_required(LogicaLecciones.ver_lecciones), name='verlecciones'),
    path('ver-temas/(?P<leccion_id>\d+)/(?P<curso_id>\d+)', login_required(LogicaLecciones.ver_temas), name="vertema"),
    path('presentacion/(?P<tema_id>\d+)', login_required(LogicaLecciones.presentacion), name="presentacion"),
    path('descargapres/(?P<tema_id>\d+)', login_required(LogicaLecciones.descargapresentacion), name="descargapres"),
    path('podcast/(?P<tema_id>\d+)', login_required(LogicaLecciones.podcast), name="podcast"),
    path('descargapod(/?P<tema_id>\d+)', login_required(LogicaLecciones.descargapodcast), name="descargapod"),
    path('codigo/(?P<tema_id>\d+)', login_required(LogicaLecciones.codigo), name="codigo"),
    path('error/', login_required(LogicaLecciones.error), name="error")
]

urlpatterns = format_suffix_patterns(urlpatterns)
