from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponse, JsonResponse

from .models import *

from art_beat.secrets import TIM_API_KEY
import json
import requests

def api(request):
    return JsonResponse({'pino': 3, 'peppolo': [1, 2, 3]})


def getSecurityCamFrame(request):
    from glob import glob
    from random import choice
    from PIL import Image

    security_images = glob("./security_images/*.jpeg")

    try:
        with open(choice(security_images), "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except:
        red_dot = Image.new('RGB', (1, 1), (255, 0, 0))
        response = HttpResponse(content_type="image/jpeg")
        red_dot.save(response, "JPEG")
        return response


def getAudioFeedback(request):
    from glob import glob
    from random import choice

    feedback_audios = glob("./feedback_audio/*.wav")

    try:
        with open(choice(feedback_audios), "rb") as f:
            return HttpResponse(f.read(), content_type="audio/wav")
    except:
        return JsonResponse({"error": "No .wav file available"})


def wav2base64string(filename):
    from base64 import b64encode
    with open(filename, "rb") as f:
        return b64encode(f.read()).decode('utf-8')


def submitSpeech(request, language="it-IT", filename="it-fede-positivo"):

    headers = {
        "apikey": TIM_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "config": {
            "language_code": language,
            "audio_channel_count": "2",
            "enableAutomaticPunctuation": "true"
        },
        "audio": {
            "content": wav2base64string("./feedback_audio/%s.wav" % filename)
        }
    }

    response = requests.post(
        "https://hackathon.tim.it/gcloudspeechtotext/v1/speech:longrunningrecognize", 
        headers=headers, 
        json=body)
        
    googleId = json.loads(response.text)['name']

    feedback = Feedback(googleId=googleId, language=language)
    feedback.save()

    return HttpResponse(content=response.text, content_type="application/json")


def retrieveSpeechesTranscripted(request):

    updated = []

    for feedback in Feedback.objects.filter(text__exact=''):
        headers = {
            "apikey": TIM_API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.get(
            "https://hackathon.tim.it/gcloudspeechtotext/v1/operations/" + feedback.googleId,
            headers=headers)

        result = json.loads(response.text)
        
        if "done" in result and result["done"] is True:
            feedback.text = result["response"]["results"][0]["alternatives"][0]["transcript"]
            feedback.confidence = result["response"]["results"][0]["alternatives"][0]["confidence"]
            feedback.save()
            updated.append(feedback.googleId)

    return JsonResponse({"updated": updated})


def runSentimentAnalysis(request):

    updated = []

    for feedback in Feedback.objects.filter(score__isnull=True):
        headers = {
            "apikey": TIM_API_KEY,
            "Content-Type": "application/json"
        }

        body = {
            "document": {
                "type": "PLAIN_TEXT",
                "content": feedback.text
            }
        }

        response = requests.post(
            "https://hackathon.tim.it/gcloudnaturallanguage/v1/documents:analyzeSentiment",
            headers=headers,
            json=body)

        result = json.loads(response.text)

        feedback.magnitude = float(result["documentSentiment"]["magnitude"])
        feedback.score = float(result["documentSentiment"]["score"])
        feedback.save()

        for sentence_res in result["sentences"]:
            sentence = Sentence()
            sentence.feedback = feedback
            sentence.text = sentence_res["text"]["content"]
            sentence.magnitude = float(sentence_res["sentiment"]["magnitude"])
            sentence.score = float(sentence_res["sentiment"]["score"])
            sentence.save()

        updated.append(result)

    return JsonResponse({"updated": updated})


def getWordCloud(request):
    from wordcloud import WordCloud

    text = " ".join([x.text for x in Sentence.objects.all()])

    wc = WordCloud(background_color="white", max_words=50, min_word_length=3)
    wc.generate(text)
    img = wc.to_image()

    response = HttpResponse(content_type="image/png")
    img.save(response, format='PNG')
    return response


def getScoreHistogram(request):
    import matplotlib.pyplot as plt 
    import seaborn as sns
    import io
    from PIL import Image

    scores = [float(x.score) for x in Feedback.objects.all()]
    
    fig = plt.figure(figsize=(4, 2), dpi=300)
    ax = sns.distplot(scores)
    fig = ax.get_figure()
    ax.set_xlim((-1.2,1.2))
    ax.set_xlabel("Feedback Scores")
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_yaxis().set_ticks([])
    ax.set_frame_on(False)
    ax.spines['bottom'].set_visible(True)
    ax.axes.get_xaxis().set_visible(True)

    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)

    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


def updateLastSecurityImage(filename, bbox):
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from PIL import Image
    import numpy as np

    im = np.array(Image.open(filename), dtype=np.uint8)

    fig,ax = plt.subplots(1)
    ax.imshow(im)

    for box in bbox:
        if box["score"] < 90:
            continue

        rect = patches.Rectangle(
                (box["x1"],box["y1"]),
                box["x2"]-box["x1"],
                box["y2"]-box["y1"],
                linewidth=1,
                edgecolor='r',
                facecolor='none')
        ax.add_patch(rect)

    plt.axis('off')

    plt.savefig("dashboard/static/last_surv_image.png",
                format="png", 
                bbox_inches="tight")


def updateCameras(request):
    from glob import glob
    from random import choice

    security_images = glob("security_images/*.jpeg")

    for camera in Camera.objects.filter(last_update__lte=timezone.now()-timedelta(seconds=300)):

        if CameraVisitors.objects.filter(datetime__gte=timezone.now()-timedelta(seconds=10)).count():
            return
        
        security_image = choice(security_images)
        response = runPedestrianDetection(security_image)

        if "people" in response:
            people = sum([x["score"] >= 90 for x in response["people"]])
            updateLastSecurityImage(security_image, response["people"])
        else:
            people = 0
        
        cv = CameraVisitors(camera=camera, visitors=people)
        cv.save()

        camera.last_update = timezone.now()
        camera.save()

        print(camera, cv,  security_image, people, response)

def runPedestrianDetection(filename="security_images/0.jpeg"):

    with open("./%s" % filename, 'rb') as f:
        data = f.read()
    
    headers = {
        'Content-Type': 'image/*',
        'apikey': TIM_API_KEY
    }
    
    response = requests.post(
        "https://hackathon.tim.it/peddetect/detect", 
        headers=headers, 
        data=data)
    
    return json.loads(response.text)
