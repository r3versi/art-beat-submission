from django.contrib import admin
from django.urls import path, include, re_path

from dashboard import views

urlpatterns = [
    path('', views.index, name='home'),
    re_path(r'^.*\.html', views.pages, name='pages'),
]
