# ocr_module.py
import logging
from google import genai

logger = logging.getLogger(__name__)

# Gemini OCR
def run_gemini_ocr(client, img, model="gemini-2.5-flash"):
    """
    Run OCR on a PIL Image using a pre-loaded Gemini client.

    Parameters:
        client: pre-loaded genai.Client
        img: PIL Image
        model: Gemini model to use (default "gemini-2.5-flash")

    Returns:
        Extracted text as string
    """
    try:
        logger.info("Gemini OCR started")
        prompt = """
        You are an OCR system.
        Extract ALL text from the image exactly as it appears.
        - Preserve line breaks
        - Preserve spacing
        - Do NOT summarize
        - Do NOT correct spelling
        - Do NOT explain anything
        Return only the raw extracted text.
        """
        response = client.models.generate_content(
            model=model,
            contents=[prompt, img]
        )
        logger.info("Gemini OCR completed successfully")
        return response.text
    except Exception as e:
        logger.exception(f"Gemini OCR failed: {e}")
        raise