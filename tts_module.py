import re
import os
from TTS.api import TTS
from pydub import AudioSegment
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Text cleaning helpers
def remove_device_lines(text):
    lines = text.splitlines()
    clean_lines = []
    for line in lines:
        stripped = line.strip()
        if re.search(r'(galaxy|iphone|samsung|redmi|pixel|oppo|vivo|huawei)', stripped, re.I):
            continue
        clean_lines.append(line)
    return "\n".join(clean_lines)

def remove_numeric_lines(text):
    lines = text.splitlines()
    clean_lines = []
    for line in lines:
        stripped = line.strip()
        if re.match(r'^\d+$', stripped):
            continue
        if re.match(r'^page\s*\d+$', stripped, re.IGNORECASE):
            continue
        if re.match(r'^\d+\s*of\s*\d+$', stripped, re.IGNORECASE):
            continue
        clean_lines.append(line)
    return "\n".join(clean_lines)

def merge_bullets(text):
    lines = text.splitlines()
    new_lines = []
    current_bullet = ""
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("•"):
            if current_bullet:
                if not re.search(r"[.;!?]$", current_bullet):
                    current_bullet += "."
                new_lines.append(current_bullet)
            current_bullet = stripped
        elif stripped == "" or stripped.startswith("Step") or stripped.isupper():
            if current_bullet:
                if not re.search(r"[.;!?]$", current_bullet):
                    current_bullet += "."
                new_lines.append(current_bullet)
                current_bullet = ""
            new_lines.append(stripped)
        else:
            if current_bullet:
                current_bullet += " " + stripped
            else:
                new_lines.append(stripped)
    if current_bullet:
        if not re.search(r"[.;!?]$", current_bullet):
            current_bullet += "."
        new_lines.append(current_bullet)
    return "\n".join(new_lines)

def normalize_headers(text):
    lines = text.splitlines()
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            new_lines.append('')
            continue
        is_header = False
        if re.match(r"^(?:\d+[\.\)]\s+|Chapter\s+\d+|Step\s+\d+)", stripped, re.IGNORECASE):
            is_header = True
        elif len(stripped.split()) <= 18 and stripped.upper() == stripped:
            is_header = True
        if is_header and not re.search(r"[.!?]$", stripped):
            stripped += '.'
        new_lines.append(stripped)
    return "\n".join(new_lines)

def fix_phone_numbers(text):
    def format_digits(match):
        return " ".join(match.group())
    return re.sub(r"\b\d{3,}\b", format_digits, text)

def fix_money(text):
    def replace_money(match):
        symbol = match.group(1)
        amount = match.group(2)
        if symbol == "£":
            return f"{amount} pounds"
        elif symbol == "$":
            return f"{amount} dollars"
        elif symbol == "€":
            return f"{amount} euros"
        return match.group()
    return re.sub(r"([£$€])\s?(\d+(?:\.\d+)?)", replace_money, text)

def fix_dates(text):
    def replace_date(match):
        raw_date = match.group()
        for fmt in ("%d/%m/%Y", "%d-%m-%Y"):
            try:
                dt = datetime.strptime(raw_date, fmt)
                return dt.strftime("%d %B %Y")
            except:
                continue
        return raw_date
    return re.sub(r"\b\d{2}[/-]\d{2}[/-]\d{4}\b", replace_date, text)

def clean_text_for_tts(text: str) -> str:
    if not text:
        return ""
    text_cleaned = (text.replace("“", '"')
                        .replace("”", '"')
                        .replace("’", "'")
                        .replace("‘", "'")
                        .replace("`", "'"))
    text_cleaned = re.sub(r"^\s*[-•*▪●]\s*", "", text_cleaned, flags=re.MULTILINE)
    text_cleaned = text_cleaned.replace(":-", ":")
    text_cleaned = re.sub(r"[^A-Za-z0-9.,!?;:'\" \n-]", "", text_cleaned)
    text_cleaned = re.sub(r'[ ]{2,}', ' ', text_cleaned)
    text_cleaned = re.sub(r'\n{2,}', '\n', text_cleaned)
    text_cleaned = re.sub(r'\s+', ' ', text_cleaned)
    return text_cleaned.strip()

def split_into_sentences(text: str, preview: bool = True) -> list:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if preview:
        for i, s in enumerate(sentences, 1):
            logger.info(f"Sentence {i}: {s}")
    return sentences


# chunk_sentences using max_chars
def chunk_sentences(sentences: list, max_chars: int = 250, preview: bool = True) -> list:
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()

        # If a single sentence is TOO long → split it safely
        if len(sentence) > max_chars:
            words = sentence.split()
            temp = ""
            for word in words:
                if len(temp) + len(word) + 1 > max_chars:
                    chunks.append(temp.strip())
                    temp = word
                else:
                    temp += " " + word
            if temp:
                chunks.append(temp.strip())
            continue

        # Normal case: add sentence to chunk
        if len(current_chunk) + len(sentence) + 1 > max_chars:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    if preview:
        for i, c in enumerate(chunks, 1):
            logger.info(f"Chunk {i} ({len(c)} chars): {c}")

    return chunks

# Orchestrate cleaning & text prep
def preprocess_text_for_tts(text: str, max_chars_per_chunk: int = 250, preview: bool = False) -> list:
    try:
        logger.info("Text processing started")
        if not text or len(text.strip()) < 3:
            logger.warning("Empty or too short text, skipping preprocessing")
            return []
        text = remove_device_lines(text)
        text = remove_numeric_lines(text)
        text = merge_bullets(text)
        text = normalize_headers(text)
        text = fix_dates(text)
        text = fix_money(text)
        text = fix_phone_numbers(text)
        text = clean_text_for_tts(text)
        sentences = split_into_sentences(text, preview=preview)
        chunks = chunk_sentences(sentences, max_chars=max_chars_per_chunk, preview=preview)
        logger.info("Text processing completed")
        return chunks
    except Exception as e:
        logger.error(f"Error during text processing: {e}", exc_info=True)
        return []

# Generate audio
def generate_audio(chunks, output_dir, tts_model):
    try:
        logger.info("Audio generation started")
        os.makedirs(output_dir, exist_ok=True)
        audio_files = []
        for idx, chunk in enumerate(chunks, 1):
            file_path = os.path.join(output_dir, f"chunk_{idx}.wav")
            tts_model.tts_to_file(text=chunk, file_path=file_path)
            audio_files.append(file_path)
        logger.info("Audio generation completed")
        return audio_files
    except Exception as e:
        logger.error(f"Error during audio generation: {e}", exc_info=True)
        return []

# Combine audio
def combine_audio(audio_files, output_path):
    try:
        logger.info("Combining audio chunks started")
        combined = AudioSegment.empty()
        for f in audio_files:
            combined += AudioSegment.from_wav(f)
        combined.export(output_path, format="wav")
        logger.info(f"Audio chunks combined and saved to: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Error during audio combining: {e}", exc_info=True)
        return None