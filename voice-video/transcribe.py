import os
import whisper
from gtts import gTTS
from playsound import playsound

AUDIO_FILE = "voice.wav"          # human voice
AI_VOICE_FILE = "ai_hindi.mp3"    # AI generated Hindi voice

# -------------------------------
# 1️⃣ LOAD WHISPER
# -------------------------------
print("🧠 Loading Whisper (medium)...")
model = whisper.load_model("medium")

# -------------------------------
# 2️⃣ HINDI TRANSCRIPTION
# -------------------------------
print("🎙️ Listening to human Hindi voice...")

result_hi = model.transcribe(
    AUDIO_FILE,
    language="hi",
    task="transcribe",
    fp16=False,
    temperature=0,
    initial_prompt="यह एक पुलिस शिकायत है। स्पष्ट हिंदी में जानकारी दी जा रही है।"
)

hindi_text = result_hi["text"].strip()

print("\n📄 HINDI TEXT (Detected):")
print(hindi_text)

# -------------------------------
# 3️⃣ HINDI → AI HINDI VOICE (TTS)
# -------------------------------
print("\n🔊 Generating AI Hindi Voice...")

tts = gTTS(text=hindi_text, lang="hi")
tts.save(AI_VOICE_FILE)

print("▶️ Playing AI Hindi Voice...")
playsound(AI_VOICE_FILE)

# -------------------------------
# 4️⃣ AI VOICE → ENGLISH TRANSLATION
# -------------------------------
print("\n🌍 Translating AI Voice to English...")

result_en = model.transcribe(
    AI_VOICE_FILE,
    language="hi",
    task="translate",
    fp16=False,
    temperature=0
)

english_text = result_en["text"].strip()

print("\n📄 FINAL ENGLISH TEXT:")
print(english_text)

# -------------------------------
# SAVE OUTPUT
# -------------------------------
with open("english_text.txt", "w", encoding="utf-8") as f:
    f.write(english_text)

print("\n🎉 DONE — AI Voice + Translation Pipeline Completed")
