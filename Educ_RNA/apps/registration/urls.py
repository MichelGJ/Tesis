from django.urls import path, re_path
from .views import login, RegistroUsuario, password, registro_usuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('login/', login_required(login), name='plogin'),
    path('registrar/', RegistroUsuario.as_view(), name='registrar'),
    path('registrousuario/', registro_usuario, name='registro'),
    path('reset/password_reset', PasswordResetView.as_view
         (template_name='registration/password_reset_form.html',
          email_template_name='registration/password_reset_email.html'), name='password_reset'),
    path('reset/password_reset_done', PasswordResetDoneView.as_view
         (template_name='registration/password_reset_done.html'), name='password_reset_done'),
    re_path('^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', PasswordResetConfirmView.as_view
            (template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done', PasswordResetCompleteView.as_view
         (template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

