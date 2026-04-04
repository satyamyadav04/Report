import os
import re
from datetime import datetime
import whisper
from playsound import playsound
import streamlit as st
from model import load_fw_model


AI_VOICE_FILE = "ai_confirm.mp3"    # AI confirmation audio

def generate_audio_evidence_id():
    now = datetime.now()
    return f"AE-{now.strftime('%Y%m%d-%H%M%S')}" 

AUDIO_EVIDENCE_ID = generate_audio_evidence_id()

model = load_fw_model()
def transcribe_hi_en(AUDIO_FILE):
    if not os.path.exists(AUDIO_FILE) or os.path.getsize(AUDIO_FILE) == 0:
        raise ValueError("Invalid audio file")

    # 1️⃣ Hindi (fast)
    hi_segments, _ = model.transcribe(
        AUDIO_FILE,
        language="hi",
        task="transcribe",
    )
    hi_text = "".join([segment.text for segment in hi_segments])

    # 2️⃣ English translation
    en_segments, _ = model.transcribe(
        AUDIO_FILE,
        task="translate"
    )
    en_text = "".join([segment.text for segment in en_segments])

    return {
        "hindi": hi_text.strip(),
        "english": en_text.strip()
    }