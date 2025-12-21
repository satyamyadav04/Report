import whisper
import os

print("🧠 Loading Whisper model...")
model = whisper.load_model("base")

audio_path = "voice.wav"

if not os.path.exists(audio_path):
    raise FileNotFoundError("❌ voice.wav not found in current folder")

print("🎙️ Transcribing + Translating...")
result = model.transcribe(audio_path, task="translate")

english_text = result["text"]

print("\n📄 English Text:")
print(english_text)

with open("english_text.txt", "w", encoding="utf-8") as f:
    f.write(english_text)

print("\n✅ English text saved as english_text.txt")
print("🎉 DONE (Hindi Speech → English Text)")
