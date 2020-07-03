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
