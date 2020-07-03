from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/", views.api, name="api"),
    path("api/getSecurityCamFrame/", views.getSecurityCamFrame),
    path("test/", views.test),
    #path("security/", views.security, name="security"),
    #path("environment/", views.environment, name="environment"),
]