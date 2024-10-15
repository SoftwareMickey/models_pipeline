from django.urls import path
from .views import MyApiView

urlpatterns = [
    path("pipeline/", MyApiView.as_view(), name="pipelining")
]