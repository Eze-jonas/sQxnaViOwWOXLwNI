import os
import logging
from flask import Flask, request, redirect, url_for, send_file, render_template_string
from PIL import Image
from TTS.api import TTS
from google import genai

from modules.pipeline_module import ocr_tts

# App setup
app = Flask(__name__)

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMP_IMAGE_FOLDER = os.path.join(BASE_DIR, "temp_images")
AUDIO_DIR = os.path.join(BASE_DIR, "audio_pipeline")

os.makedirs(TEMP_IMAGE_FOLDER, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# Load Gemini client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not set!")

client = genai.Client(api_key=api_key)
logger.info("Gemini client loaded.")

# Load TTS Model
tts = None

def get_tts():
    global tts
    if tts is None:
        logger.info("Loading TTS model...")
        tts = TTS(
            model_name="tts_models/en/ljspeech/tacotron2-DDC",
            gpu=False
        )
        logger.info("TTS model loaded.")
    return tts


INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>OCR → TTS App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <script>
        function showSpinner() {
            document.getElementById("spinner").style.display = "block";
        }
    </script>
</head>
<body class="bg-light">
<div class="container mt-5">
    <h2>Upload Image</h2>

    <form method="POST" action="/process" enctype="multipart/form-data" onsubmit="showSpinner()">
        <input class="form-control mb-3" type="file" name="image" required>
        <button class="btn btn-primary">Process</button>
    </form>

    <div id="spinner" class="alert alert-info" style="display:none;">
        Processing...
    </div>
</div>
</body>
</html>
"""

RESULT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Result</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-5">

    <h3>{{ filename }}</h3>

    {% if audio_file %}
        <p class="text-success">Audio generated</p>

        <audio controls class="w-100 mb-3">
            <source src="{{ url_for('get_audio', filename=audio_filename) }}" type="audio/wav">
        </audio>

        <a href="{{ url_for('get_audio', filename=audio_filename) }}" class="btn btn-success">
            Download
        </a>
    {% else %}
        <p class="text-danger">Failed to generate audio</p>
    {% endif %}

    <br><br>
    <a href="/" class="btn btn-secondary">Back</a>

</div>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(INDEX_HTML)


@app.route("/process", methods=["POST"])
def process_image():
    file = request.files.get("image")

    if not file or not file.filename:
        return redirect(url_for("index"))

    temp_path = os.path.join(TEMP_IMAGE_FOLDER, file.filename)
    file.save(temp_path)

    logger.info(f"Processing: {file.filename}")

    try:
        img = Image.open(temp_path)

        audio_filename = f"{os.path.splitext(file.filename)[0]}.wav"
        audio_file_path = os.path.join(AUDIO_DIR, audio_filename)

        audio_file = ocr_tts(
            img=img,
            gemini_client=client,
            tts_model=get_tts(),
            audio_dir=AUDIO_DIR,
            final_audio_file=audio_file_path,
            preview=False
        )

    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")
        audio_file = None

    try:
        os.remove(temp_path)
    except:
        pass

    return render_template_string(
        RESULT_HTML,
        filename=file.filename,
        audio_file=bool(audio_file),
        audio_filename=audio_filename
    )


@app.route("/audio/<filename>")
def get_audio(filename):
    return send_file(os.path.join(AUDIO_DIR, filename), as_attachment=True)


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False") == "True"
    print(f"\nFlask app running at http://0.0.0.0:5000 | debug={debug_mode}\n")
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
    