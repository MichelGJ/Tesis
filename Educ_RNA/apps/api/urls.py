from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import login, RegistrarUsuario, ActualizarUsuario, VerLecciones, VerTemas, CambioContrasena, VerInfoTema, \
    VerLinksPresentaciones, VerLinkPodcast, GetQuiz, GetPreguntaQuiz, GetRespuesta, GetPrueba, GetPreguntaPrueba,\
    GetPreguntaId, GetRespuestaId, ConsultarProgreso, RegistrarProgreso,  ActualizarProgreso, VerLeccionId, VerTemaId, \
    RegistrarCalificacion, ConsultarCalificacion, GetPruebaId, ActualizarCalificacion, ConsultarCalificacionPrueba
from rest_auth.views import PasswordResetView, PasswordResetConfirmView

# Direcciones URL del API

urlpatterns = {
    path('login/', login, name="login"),
    path('ver-lecciones/', VerLecciones.as_view(), name="verlec"),
    path('ver-temas/<leccion_id>', VerTemas.as_view(), name="vertemas"),
    path('ver-infotemas/<tema_id>', VerInfoTema.as_view(), name="verinfotema"),
    path('registrar-usuario/', RegistrarUsuario.as_view(), name="registrarusuario"),
    path('actualizar-usuario/<id>', ActualizarUsuario.as_view(), name="actualizarusuario"),
    path('cambio-contrasena/', CambioContrasena.as_view(), name="cambiocontrasena"),
    path('ver-linkspresent/<tema_id>', VerLinksPresentaciones.as_view(), name="verpresentaciones"),
    path('ver-linkpod/<tema_id>', VerLinkPodcast.as_view(), name="verpodcast"),
    path('ver-quiz/<tema_id>', GetQuiz.as_view(), name="verquiz"),
    path('ver-prueba/<leccion_id>', GetPrueba.as_view(), name="verprueba"),
    path('ver-pruebaid/<id>', GetPruebaId.as_view(), name="verprueba"),
    path('ver-pregquiz/<quiz_id>', GetPreguntaQuiz.as_view(), name="verpregquiz"),
    path('ver-pregprueba/<prueba_id>', GetPreguntaPrueba.as_view(), name="verpregprueba"),
    path('ver-pregunta/<id>', GetPreguntaId.as_view(), name="verpregunta"),
    path('ver-resp/<pregunta_id>', GetRespuesta.as_view(), name="verresp"),
    path('ver-respid/<id>', GetRespuestaId.as_view(), name="verrespid"),
    path('ver-progreso/<usuario_id>', ConsultarProgreso.as_view(), name="verprogreso"),
    path('registrar-progreso/', RegistrarProgreso.as_view(), name="registrarprogreso"),
    path('actualizar-progreso/', ActualizarProgreso.as_view(), name="actualizarprogreso"),
    path('ver-leccion/<id>', VerLeccionId.as_view(), name='verleccionid'),
    path('ver-tema/<id>', VerTemaId.as_view(), name='vertemaid'),
    path('registrar-calificacion/', RegistrarCalificacion.as_view(), name='registrarcalificacion'),
    path('actualizar-calificacion/', ActualizarCalificacion.as_view(), name='actualizarcalificacion'),
    path('ver-calificacion/<usuario_id>', ConsultarCalificacion.as_view(), name='vercalificacion'),
    path('ver-calificacionprueba/<usuario_id>/<prueba_id>', ConsultarCalificacionPrueba.as_view(), name='vercalificacion')
}

urlpatterns = format_suffix_patterns(urlpatterns)
