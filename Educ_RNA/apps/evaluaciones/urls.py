from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import LogicaEvaluaciones

urlpatterns = [
    path('instrucciones/?id=<tema_id>/?id=<leccion_id>/?id=<curso_id>', login_required(LogicaEvaluaciones.instrucciones), name='instrucciones'),
    path('quiz/?id=<tema_id>', login_required(LogicaEvaluaciones.quiz), name='quiz'),
    path('quiz2/?r_id=<respuesta_id>/?p_id=<pregunta_id>/?p_id=<tema_id>', login_required(LogicaEvaluaciones.corregirquiz), name='quiz2'),
    path('examen/?id=<leccion_id>', login_required(LogicaEvaluaciones.examen), name='examen'),
    path('examen2/?r_id=<respuesta_id>/?p_id=<leccion_id>',
         login_required(LogicaEvaluaciones.examen2), name='examen2'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
