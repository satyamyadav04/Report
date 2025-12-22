import subprocess
import os
import whisper
from googletrans import Translator

VIDEO_FILE = "video.avi"
AUDIO_FILE = "voice.wav"

# -------------------------------
# 1️⃣ CHECK VIDEO
# -------------------------------
if not os.path.exists(VIDEO_FILE):
    raise FileNotFoundError("❌ video.avi not found")

print("🎞️ Extracting clean audio from video...")

# -------------------------------
# 2️⃣ VIDEO → CLEAN AUDIO
# -------------------------------
ffmpeg_cmd = [
    "ffmpeg",
    "-y",
    "-i", VIDEO_FILE,
    "-vn",
    "-ac", "1",
    "-ar", "16000",
    "-af", "afftdn,volume=1.5",
    AUDIO_FILE
]

subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if not os.path.exists(AUDIO_FILE):
    raise RuntimeError("❌ Audio extraction failed")

print("✅ Clean audio ready")

# -------------------------------
# 3️⃣ HINDI TRANSCRIPTION (NO TRANSLATE)
# -------------------------------
print("🧠 Loading Whisper (medium model)...")
model = whisper.load_model("medium")

print("🎙️ Transcribing Hindi speech...")
result_hi = model.transcribe(
    AUDIO_FILE,
    language="hi",
    task="transcribe",
    fp16=False,
    temperature=0
)

hindi_text = result_hi["text"].strip()

print("\n📄 HINDI TEXT:")
print(hindi_text)

with open("hindi_text.txt", "w", encoding="utf-8") as f:
    f.write(hindi_text)

# -------------------------------
# 4️⃣ HINDI → ENGLISH TRANSLATION
# -------------------------------
print("\n🌍 Translating to English...")
translator = Translator()
eng = translator.translate(hindi_text, src="hi", dest="en")

english_text = eng.text.strip()

print("\n📄 ENGLISH TEXT:")
print(english_text)

with open("english_text.txt", "w", encoding="utf-8") as f:
    f.write(english_text)

print("\n🎉 DONE — Accurate Translation Completed")
