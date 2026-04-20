# pipeline_module.py
print("pipeline_module.py is starting...")

import os
import logging
from modules.ocr_module import run_gemini_ocr
from modules.tts_module import preprocess_text_for_tts, generate_audio, combine_audio

# Logger (NO config here)
logger = logging.getLogger(__name__)

# Orchestrate functions on ocr and tts modules with a function;ocr_tts.
def ocr_tts(img, gemini_client, tts_model, audio_dir=None, final_audio_file=None, preview=False):
    try:
        logger.info("OCR → TTS pipeline started")

        # Setup audio paths
        if audio_dir is None:
            audio_dir = os.path.join(os.getcwd(), "audio_temp")
        if final_audio_file is None:
            final_audio_file = os.path.join(audio_dir, "full_audio.wav")
        os.makedirs(audio_dir, exist_ok=True)

        # Function from ocr module.
        ocr_text = run_gemini_ocr(gemini_client, img)
        if not ocr_text.strip():
            logger.error("No text extracted by Gemini OCR.")
            return None
        logger.info("OCR text preview:\n" + ocr_text[:300])

        # Functions from tts module.
        chunks = preprocess_text_for_tts(ocr_text, preview=preview)

        if not chunks:
            logger.error("No chunks generated.")
            return None

        logger.info(f"{len(chunks)} chunks generated.")

        # Generate audio
        audio_files = generate_audio(chunks, audio_dir, tts_model)

        if not audio_files:
            logger.error("Audio generation failed.")
            return None

        # Combine audio
        final_audio = combine_audio(audio_files, final_audio_file)

        if not final_audio:
            logger.error("Audio combining failed.")
            return None

        logger.info(f"Pipeline completed successfully: {final_audio}")
        return final_audio

    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")
        return None