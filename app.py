from flask import Flask, request, jsonify
import os
import requests
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import aiplatform_v1beta1 as aiplatform

app = Flask(__name__)

# Set Google Cloud credentials environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "users/ameera/documents/smiling-box-418820-6de1ebd24a07.json"

# Gemini AI API endpoint URLs
PARAPHRASE_ENDPOINT = "https://api.gemini.ai/paraphrase"
SUMMARIZE_ENDPOINT = "https://api.gemini.ai/summarize"

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
    # Create a client for interacting with the Gemini AI API
    client = aiplatform.gapic.PredictionServiceClient()

    # Set the endpoint for the API
    client.transport.endpoint = "us-central1-aiplatform.googleapis.com:443"

    # Set the location of the model
    location = "us-central1"

    # Set the parameters for the prediction
    parameters_dict = {}

    # Set the input data for the prediction
    instance = aiplatform.gapic.schema.predict.instance.TextExtractionPredictionInstance(
        content=text,
        mime_type="text/plain"  # The MIME type of the input text
    ).to_value()

    # Perform the prediction
    response = client.predict(
        endpoint=f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/{location}/models/text-bison-001",
        instances=[instance],
        parameters_dict=parameters_dict,
    )

    # Extract the predicted text
    predicted_text = response.predictions[0].text_extraction.paraphrase.content

    return predicted_text

def summarize_text(text):
    # Create a client for interacting with the Gemini AI API
    client = aiplatform.gapic.PredictionServiceClient()

    # Set the endpoint for the API
    client.transport.endpoint = "us-central1-aiplatform.googleapis.com:443"

    # Set the location of the model
    location = "us-central1"

    # Set the parameters for the prediction
    parameters_dict = {}

    # Set the input data for the prediction
    instance = aiplatform.gapic.schema.predict.instance.TextExtractionPredictionInstance(
        content=text,
        mime_type="text/plain"  # The MIME type of the input text
    ).to_value()

    # Perform the prediction
    response = client.predict(
        endpoint=f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/{location}/models/text-bison-001",
        instances=[instance],
        parameters_dict=parameters_dict,
    )

    # Extract the predicted text
    predicted_text = response.predictions[0].text_extraction.summary.content

    return predicted_text

@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")

@app.route("/upload", methods=["POST"])
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
    app.run(debug=True, port=5000)
