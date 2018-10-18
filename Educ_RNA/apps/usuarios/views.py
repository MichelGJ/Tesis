from django.shortcuts import render
from django.http import HttpResponse
import requests
from apps.usuarios.forms import BucketForm
# Create your views here.

def index(request):
    return render(request, 'usuarios/index.html')

