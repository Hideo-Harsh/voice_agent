from django.urls import path
from .views import VoiceQueryView

urlpatterns = [
    path("ask/", VoiceQueryView.as_view(), name="ask"),
]
