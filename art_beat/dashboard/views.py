from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
from django.views.generic.list import ListView

from .models import *
from math import floor


def index(request):
    return render(request, "index.html")


def security(request):
    out_rooms = []

    for room in Room.objects.all():
        visitors = 0
        last_update = None
        for camera in Camera.objects.filter(room=room):
            visitors += CameraVisitors.objects.filter(camera=camera).last().visitors
            if last_update is None or camera.last_update > last_update: 
                last_update = camera.last_update
        
        room.last_update = last_update
        room.visitors = visitors
        room.capacity = int(floor(room.mq / 7.0))

        out_rooms.append(room)

    context = {"rooms": out_rooms}
    return render(request, "security.html", context)


def feedbacks(request):
    context = {"feedbacks": []}
    for feedback in Feedback.objects.all():
        sentences = Sentence.objects.filter(feedback=feedback)
        context["feedbacks"].append({"feedback": feedback, "sentences": sentences})
    
    return render(request, "feedbacks.html", context)


def environment(request):
    import numpy as np

    out_rooms = []
    
    for room in Room.objects.all():
        light_on = False
        for camera in Camera.objects.filter(room=room):
            light_on = light_on or (CameraVisitors.objects.filter(camera=camera).last().visitors > 0)

        room.light_on = light_on    
        room.temperature = np.clip(round(np.random.normal(22, 5), 1), 15, 35)
        room.humidity = np.clip(round(np.random.normal(50, 20), 1),0,100)

        room.is_temp_ok = room.temperature > 16 and room.temperature < 28
        room.is_hum_ok = room.humidity > 35 and room.humidity < 65

        out_rooms.append(room)
    
    context = {"rooms": out_rooms}

    return render(request, "environment.html", context)

def audience(request):
    context = {}
    return render(request, "audience.html", context)


def page404(request):
    context = {}
    return render(request, "error-404.html", context)


