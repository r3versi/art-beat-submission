from django.urls import path,re_path

from . import views
from . import apis

urlpatterns = [
    path("", views.index, name="index"),
    path("api/", apis.api, name="api"),

    path("api/getSecurityCamFrame/", apis.getSecurityCamFrame),
    path("api/getAudioFeedback/", apis.getAudioFeedback),
    path("api/submitSpeech/<slug:language>/<slug:filename>", apis.submitSpeech),
    path("api/submitImage", apis.submitImage),
    path("api/retrieveSpeechesTranscripted", apis.retrieveSpeechesTranscripted),
    path("api/runSentimentAnalysis", apis.runSentimentAnalysis),
    path("api/getWordCloud", apis.getWordCloud, name="get-word-cloud"),
    path("api/getScoreHistogram", apis.getScoreHistogram, name="get-score-histogram"),
    
    path("feedbacks/", views.feedbacks, name="feedbacks"),
    path("security/", views.security, name="security"),
    path("environment/", views.environment, name="environment"),
    path("audience/", views.audience, name="audience"),

    re_path(r"^.*$", views.page404),
]
