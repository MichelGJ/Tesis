from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import LogicaEvaluaciones

urlpatterns = [
    path('instrucciones/?id=<tema_id>', login_required(LogicaEvaluaciones.instrucciones_quiz), name='instruccionesquiz'),
    path('quiz/?id=<tema_id>', login_required(LogicaEvaluaciones.quiz), name='quiz'),
    path('quiz2/?r_id=<respuesta_id>/?p_id=<pregunta_id>/?p_id=<tema_id>', login_required(LogicaEvaluaciones.corregirquiz), name='quiz2'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
