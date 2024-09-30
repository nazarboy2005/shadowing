# transcription/views.py

from django.http import JsonResponse
import assemblyai as aai


# Set your API key for AssemblyAI
aai.settings.api_key = "848c053f81c048afac92630daf4b41c7"


def transcribe_video(request):
    if request.method == "POST":
        video_url = request.POST.get('video_url')

        if not video_url:
            return JsonResponse({'error': 'Video URL is required.'}, status=400)

        try:
            # Create a transcriber instance
            transcriber = aai.Transcriber()

            # Transcribe the video (this sends a request to AssemblyAI)
            transcript_response = transcriber.transcribe(video_url)

            return JsonResponse({
                'status': 'success',
                'transcript': transcript_response['text']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
