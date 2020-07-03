from django.contrib import admin
from django.urls import path, include, re_path

# from dashboard import views

from dashboard import views

urlpatterns = [
    path('', include('dashboard.urls')),
]
