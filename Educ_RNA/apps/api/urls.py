from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import login, RegistrarUsuario, ActualizarUsuario, VerLecciones, VerTemas, CambioContrasena, VerInfoTema, VerLinksPresentaciones
from rest_auth.views import PasswordResetView, PasswordResetConfirmView

# Direcciones URL del API

urlpatterns = {
    path('login/', login, name="create"),
    path('ver-lecciones/', VerLecciones.as_view(), name="verlec"),
    path('ver-temas/<leccion_id>', VerTemas.as_view(), name="vertema"),
    path('ver-infotemas/<tema_id>', VerInfoTema.as_view(), name="verinfotema"),
    path('registrar-usuario/', RegistrarUsuario.as_view(), name="registrarusuario"),
    path('actualizar-usuario/<id>', ActualizarUsuario.as_view(), name="actualizarusuario"),
    path('cambio-contrasena/', CambioContrasena.as_view(), name="cambiocontrasena"),
    path('ver-linkspresent/<tema_id>', VerLinksPresentaciones.as_view(), name="verpresentaciones"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
