"""Educ_RNA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.registration.views import login
from django.contrib.auth.views import logout_then_login

urlpatterns = [
    path('', login, name="login"),
    path('logout/', logout_then_login, name='logout'),
    path('accounts/login/', login, name="rlogin"),
    path('admin/', admin.site.urls),
    path('usuarios/', include('apps.usuarios.urls')),
    path('registration/', include('apps.registration.urls')),
    path('api/', include('apps.api.urls')),
    path('lecciones/', include('apps.lecciones.urls')),
    path('evaluaciones/', include('apps.evaluaciones.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls'))
]
