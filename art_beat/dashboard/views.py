from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
from django.views.generic.list import ListView

from .models import Feedback, Sentence



def index(request):
    return render(request, "index.html")


def security(request):
    context = {}
    return render(request, "security.html", context)


def feedbacks(request):
    context = {"feedbacks": []}
    for feedback in Feedback.objects.all():
        sentences = Sentence.objects.filter(feedback=feedback)
        context["feedbacks"].append({"feedback": feedback, "sentences": sentences})
    
    return render(request, "feedbacks.html", context)


def environment(request):
    context = {}
    return render(request, "environment.html", context)

def audience(request):
    context = {}
    return render(request, "audience.html", context)


def page404(request):
    context = {}
    return render(request, "error-404.html", context)


def image2base64string(filename):
    from base64 import b64encode
    with open(filename, "rb") as file:
        return b64encode(file.read()).decode('utf-8')


def submitImage ():
    import requests
    
    URL = "https://hackathon.tim.it/peddetect/detect"
    filename = "C:/Users/alexi/Desktop/progs/Git/art-beat/art_beat/security_images/0.jpeg"
    PEDESTRIAN_API_KEY = "U2FRGRrBNxEHANXheJcKmhbK0v5CyVPT"
    
    headers = {
        'Content-Type': 'image/*',
        'apikey': PEDESTRIAN_API_KEY
        }
    
    # body = {
    #         image2base64string(filename)
    #     }
    
    data = image2base64string(filename)
    
    response = requests.post(URL, headers = headers, data = data)
    #response = requests.post(URL, headers = headers, json = body)
    #return HttpResponse(content = response.text, content_type = "application/json")
    
    print("Status code: {}".format(response.status_code))
    print("Header: {}".format(response.headers))
    print("Text: {}".format(response.text))
