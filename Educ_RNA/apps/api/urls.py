from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import login, ver_lecciones, RegistrarUsuario, ActualizarUsuario, VerLecciones, VerLeccion, VerTemas, \
    CambioContrasena
from rest_auth.views import PasswordResetView, PasswordResetConfirmView

# Direcciones URL del API

urlpatterns = {
    path('login/', login, name="create"),
    path('ver-lecciones/', ver_lecciones, name="verlec"),
    path('ver-lecciones2/', VerLecciones.as_view(), name="verlec2"),
    path('ver-leccion/(<id>)', VerLeccion.as_view(), name="verlec3"),
    path('ver-temas/(<leccion_id>)', VerTemas.as_view(), name="vertema"),
    path('registrar-usuario/', RegistrarUsuario.as_view(), name="registrarusuario"),
    path('actualizar-usuario/(<id>)', ActualizarUsuario.as_view(), name="actualizarusuario"),
    path('cambio-contrasena/', CambioContrasena.as_view(), name="cambiocontrasena"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
