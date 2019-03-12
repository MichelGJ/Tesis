from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class ModificarUsuarioForm(UserChangeForm):
    class Meta:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
        ]
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }

    def __init__(self, *args, **kwargs):
        super(ModificarUsuarioForm, self).__init__(*args, **kwargs)
        del self.fields['password']
