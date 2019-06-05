from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import LogicaEvaluaciones

urlpatterns = [
    path('instrucciones/(?P<tema_id>\d+)/(?P<leccion_id>\d+)/(?P<curso_id>\d+)', login_required(LogicaEvaluaciones.instrucciones), name='instrucciones'),
    path('quiz/(?P<tema_id>\d+)', login_required(LogicaEvaluaciones.quiz), name='quiz'),
    path('quiz2/(?P<respuesta_id>\d+)/(?P<pregunta_id>\d+)/(?P<tema_id>\d+)', login_required(LogicaEvaluaciones.corregirquiz), name='quiz2'),
    path('examen/(?P<leccion_id>\d+)', login_required(LogicaEvaluaciones.examen), name='examen'),
    path('examen2/(?P<respuesta_id>\d+)/(?P<leccion_id>\d+)',
         login_required(LogicaEvaluaciones.examen2), name='examen2'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
