# transcription/urls.py

from django.urls import path
from .views import transcribe_video

app_name = 'transcription'

urlpatterns = [
    path('transcribe/', transcribe_video, name='transcribe_video'),
]
