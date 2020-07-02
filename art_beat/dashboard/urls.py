from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("security/", views.security, name="security"),
    path("environment/", views.environment, name="environment"),
]