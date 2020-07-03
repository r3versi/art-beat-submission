from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template

from PIL import Image

# Create your views here.
#@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('error-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('error-500.html')
        return HttpResponse(html_template.render(context, request))


def getSecurityCamFrame(request):
    from glob import glob
    from random import choice

    security_images = glob("./security_images/*.jpeg")
    
    try:
        with open(choice(security_images), "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except:
        red_dot = Image.new('RGB', (1, 1), (255, 0, 0))
        response = HttpResponse(content_type="image/jpeg")
        red_dot.save(response, "JPEG")
        return response


def api(request):
    return JsonResponse({'pino':3,'peppolo':[1,2,3]})


def wav2base64string(filename): 
    from base64 import b64encode
    with open(filename, "rb") as f:
        return b64encode(f.read()).decode('utf-8')


def submitSpeech(request):
    from art_beat.secrets import TIM_API_KEY

    import requests

    headers = {
        "apikey": TIM_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "config": {
            "language_code": "it-IT",
            "audio_channel_count": "2"
        },
        "audio": {
            "content": wav2base64string("./feedback_audio/0.wav")
        }
    }

    response = requests.post("https://hackathon.tim.it/gcloudspeechtotext/v1/speech:longrunningrecognize", headers=headers, json=body)
    return HttpResponse(content=response.text, content_type="application/json")


def security(request):
    pass
