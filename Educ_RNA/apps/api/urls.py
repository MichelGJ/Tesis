from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, login


urlpatterns = {
    path('bucketlists/', CreateView.as_view(), name="create"),
    path('login/', login, name="create"),
}

urlpatterns = format_suffix_patterns(urlpatterns)