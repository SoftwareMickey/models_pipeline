from django.urls import path
from .views import *

urlpatterns = [
    path("pipeline/", MyApiView.as_view(), name = "pipelining"),
    path("deploy/", DeploymentView.as_view(), name = "deployment"),
    path("predict/", PredictionView.as_view(), name="predict")
]