from django import forms
from apps.api.models import Bucketlist
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class BucketForm(forms.ModelForm):

    class Meta:
        model = Bucketlist

        fields = [
            'name',
        ]

        labels = {
            'name': 'Name',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
