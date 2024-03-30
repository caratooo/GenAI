from flask import Flask, request, jsonify
import os
import requests
from google.cloud import speech_v1p1beta1 as speech

app = Flask(__name__)

# Set Google Cloud credentials environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "users/ameera/documents/smiling-box-418820-6de1ebd24a07.json"

# Gemini AI API endpoint URLs
PARAPHRASE_ENDPOINT = "https://api.gemini.ai/paraphrase"
SUMMARIZE_ENDPOINT = "https://api.gemini.ai/summarize"

# Gemini AI API key
API_KEY = "your-api-key"

def transcribe_audio(audio_file):
    client = speech.SpeechClient()

    # Upload audio file to Google Cloud Storage
    audio = speech.RecognitionAudio(uri=f'gs://your-bucket-name/{audio_file}')

    # Configure audio settings
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # Perform speech-to-text transcription
    response = client.recognize(config=config, audio=audio)

    # Extract transcribed text
    transcribed_text = ""
    for result in response.results:
        transcribed_text += result.alternatives[0].transcript

    return transcribed_text

def paraphrase_text(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "text": text
    }
    response = requests.post(PARAPHRASE_ENDPOINT, json=data, headers=headers)
    return response.json()

def summarize_text(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "text": text
    }
    response = requests.post(SUMMARIZE_ENDPOINT, json=data, headers=headers)
    return response.json()

@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    uploaded_file = request.files["mediaFile"]
    audio_path = "/path/to/save/uploaded/audio_file.wav"  # Update with the path to save the uploaded audio file
    uploaded_file.save(audio_path)

    # Perform audio transcription
    transcribed_text = transcribe_audio(audio_path)

    # Perform paraphrasing
    paraphrased_result = paraphrase_text(transcribed_text)

    # Perform summarization
    summarized_result = summarize_text(transcribed_text)

    return jsonify({
        "transcribed_text": transcribed_text,
        "paraphrased_result": paraphrased_result,
        "summarized_result": summarized_result
    })

if __name__ == "__main__":
    app.run(debug=True)
