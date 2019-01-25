from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UsuarioForm(UserCreationForm):

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
        ]
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo',
            'username': 'Usuario',
        }
