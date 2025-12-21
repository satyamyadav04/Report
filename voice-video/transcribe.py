import subprocess
import os
import whisper

VIDEO_FILE = "../video.avi"
AUDIO_FILE = "../voice.wav"

# 1️⃣ Check video exists
if not os.path.exists(VIDEO_FILE):
    raise FileNotFoundError("❌ input_video.mp4 not found")

print("🎞️ Extracting clean audio from video...")

# 2️⃣ Extract + clean audio using FFmpeg
command = [
    "ffmpeg",
    "-y",
    "-i", VIDEO_FILE,
    "-vn",
    "-ac", "1",
    "-ar", "16000",
    "-af", "highpass=f=200, lowpass=f=3000, afftdn",
    AUDIO_FILE
]

subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if not os.path.exists(AUDIO_FILE):
    raise RuntimeError("❌ Audio extraction failed")

print("✅ Clean audio extracted")

# 3️⃣ Load Whisper
print("🧠 Loading Whisper model (base)...")
model = whisper.load_model("base")

# 4️⃣ Transcribe + Translate
print("🎙️ Transcribing (Hindi → English)...")

result = model.transcribe(
    AUDIO_FILE,
    task="translate",
    language="hi",
    fp16=False,
    temperature=0
)

text = result["text"].strip()

# 5️⃣ Save output
with open("final_transcript.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("\n📄 FINAL TRANSCRIPT:")
print(text)

print("\n✅ Saved as final_transcript.txt")
print("🎉 DONE")
