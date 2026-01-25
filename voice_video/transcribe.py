import os
import re
from datetime import datetime
import whisper
from gtts import gTTS
from playsound import playsound
import streamlit as st
from model import load_model


AI_VOICE_FILE = "ai_confirm.mp3"    # AI confirmation audio

def generate_audio_evidence_id():
    now = datetime.now()
    return f"AE-{now.strftime('%Y%m%d-%H%M%S')}" 

AUDIO_EVIDENCE_ID = generate_audio_evidence_id()

@st.cache_resource
def get_model(model_name="small"):
    return load_model(model_name)

model = load_model()
def transcribe_pipline(AUDIO_FILE):
    if not os.path.exists(AUDIO_FILE):
        raise FileNotFoundError(f"Audio file not found: {AUDIO_FILE}")
    
    file_size = os.path.getsize(AUDIO_FILE)
    if file_size == 0:
        raise ValueError(f"Audio file is empty: {AUDIO_FILE}")
    
    try:
        result = model.transcribe(
            AUDIO_FILE,
            fp16=False,
            temperature=0
        )
    except RuntimeError as e:
        if "cannot reshape tensor" in str(e):
            raise ValueError(f"Invalid or corrupted audio file. The audio might be too short, silent, or in an unsupported format. Original error: {e}")
        raise
    
    input_language = result.get("language", "unknown")
    original_text = result["text"].strip()
    return original_text, input_language

# def generate_ai_confirmation(text, lang):
#     tts_lang = lang if lang in ["hi", "en"] else "hi"
#     tts = gTTS(text=text, lang=tts_lang)
#     tts.save(AI_VOICE_FILE)
#     return AI_VOICE_FILE

def confirmed_audio_to_text(AUDIO_FILE):
    hi = model.transcribe(AUDIO_FILE, language="hi", fp16=False)["text"]
    en = model.transcribe(AUDIO_FILE, task="translate", language="en", fp16=False)["text"]
    
    return {
        "hindi": hi.strip(),
        "english": en.strip()
    }