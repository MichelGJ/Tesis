from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.views import auth_login
from django.http import HttpResponse, JsonResponse
# Create your views here.
from rest_framework import generics
from .serializers import BucketlistSerializer
from .models import Bucketlist
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status


class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()


@method_decorator(csrf_exempt)
def login(request):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    user = authenticate(username=username, password=password)
    if user is not None:
        data = {'user': str(user)}
        return JsonResponse(data, status=200)
    else:
        return HttpResponse(status=404)
