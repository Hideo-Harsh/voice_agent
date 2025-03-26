import os
import whisper
import openai
from pydub import AudioSegment
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

class VoiceQueryView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # Accept audio files

    def post(self, request):
        if "audio" not in request.FILES:
            return Response({"error": "No audio file provided"}, status=400)

        audio_file = request.FILES["audio"]

        # Load Whisper model
        model = whisper.load_model("base")

        # Save the file temporarily
        temp_audio_path = "temp_audio.mp3"
        with open(temp_audio_path, "wb") as f:
            f.write(audio_file.read())

        # Transcribe the audio
        result = model.transcribe(temp_audio_path)
        user_query = result["text"]

        # Call OpenAI GPT API
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_query}]
        )

        ai_response = response.choices[0].message.content

        # Convert text to speech using OpenAI TTS
        speech_file_path = os.path.join(settings.MEDIA_ROOT, "response_audio.mp3")

        tts_response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=ai_response
        )

        # Save the TTS response as an audio file in MEDIA_ROOT
        with open(speech_file_path, "wb") as f:
            f.write(tts_response.content)

        return Response({
            "text": user_query,
            "ai_response": ai_response,
            "audio_url": f"{settings.MEDIA_URL}response_audio.mp3"
        }, status=200)
