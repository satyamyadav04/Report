import os
import re
from datetime import datetime
import whisper
from gtts import gTTS
from playsound import playsound

# ==================================================
# FILES (IMPORTANT FIX: mp3, not wav)
# ==================================================
AUDIO_FILE = "voice.wav"            # user input voice (already recorded)
AI_VOICE_FILE = "ai_confirm.mp3"    # ✅ AI confirmation audio (MP3)
REPORT_FILE = "final_report.txt"

# ==================================================
# 1️⃣ LOAD WHISPER
# ==================================================
print("🧠 Loading Whisper (medium)...")
model = whisper.load_model("medium")

# ==================================================
# 2️⃣ USER VOICE → TEXT (AUTO LANGUAGE)
# ==================================================
print("🎙️ Processing user voice...")

result = model.transcribe(
    AUDIO_FILE,
    fp16=False,
    temperature=0
)

input_language = result.get("language", "unknown")
original_text = result["text"].strip()

print("\n📄 ORIGINAL TEXT (User Language):")
print(original_text)
print(f"🌐 Detected Language: {input_language}")

with open("original_text.txt", "w", encoding="utf-8") as f:
    f.write(original_text)

# ==================================================
# 3️⃣ AI CONFIRMATION AUDIO (SAME LANGUAGE AS INPUT)
# ==================================================
print("\n🔊 Generating AI confirmation audio (same language)...")

# safety fallback
tts_language = input_language if input_language in ["hi", "en"] else "hi"

tts = gTTS(
    text=original_text,        # ✅ SAME language text
    lang=tts_language,
    tld="co.in" if tts_language == "hi" else "com"
)

tts.save(AI_VOICE_FILE)

print("▶️ Playing AI confirmation audio...")
playsound(AI_VOICE_FILE)

# ==================================================
# 4️⃣ ALL FURTHER PROCESS FROM AI CONFIRMED AUDIO
# ==================================================
print("\n🧠 Processing confirmed AI audio...")

# ---------- Hindi ----------
result_hi = model.transcribe(
    AI_VOICE_FILE,
    task="translate",
    language="hi",
    fp16=False
)
hindi_text = result_hi["text"].strip()

with open("hindi_text.txt", "w", encoding="utf-8") as f:
    f.write(hindi_text)

# ---------- English ----------
result_en = model.transcribe(
    AI_VOICE_FILE,
    task="translate",
    language="en",
    fp16=False
)
english_text = result_en["text"].strip()

with open("english_text.txt", "w", encoding="utf-8") as f:
    f.write(english_text)

# ==================================================
# 5️⃣ FIELD EXTRACTION (UNCHANGED LOGIC)
# ==================================================
def extract_report_fields(hindi_text):
    fields = {}

    name_patterns = [
        r"मेरा नाम ([^,।]+)",
        r"नाम ([^,।]+)"
    ]

    fields["NAME"] = "Not Mentioned"
    for p in name_patterns:
        m = re.search(p, hindi_text)
        if m:
            fields["NAME"] = m.group(1).strip()
            break

    city_match = re.search(r"(दिल्ली|मुंबई|लखनऊ|पटना|कानपुर)", hindi_text)
    fields["PLACE"] = city_match.group(1) if city_match else "Not Mentioned"

    place_patterns = [
        "रेलवे स्टेशन", "बस स्टैंड", "मेट्रो स्टेशन",
        "बाज़ार", "मार्केट", "पार्क", "मॉल", "थाना"
    ]

    fields["INCIDENT_PLACE"] = "Not Mentioned"
    for p in place_patterns:
        if p in hindi_text:
            fields["INCIDENT_PLACE"] = p
            break

    fields["COMPLAINT_TYPE"] = (
        "Mobile Theft Complaint" if "चोरी" in hindi_text else "General Complaint"
    )

    now = datetime.now()
    fields["DATE"] = now.strftime("%d-%m-%Y")
    fields["TIME"] = now.strftime("%H:%M")

    return fields

fields = extract_report_fields(hindi_text)

# ==================================================
# 6️⃣ USER CHOICE FOR REPORT LANGUAGE
# ==================================================
print("\n📘 Report language choose kare:")
print("👉 Hindi ke liye: hi")
print("👉 English ke liye: en")

choice = input("Your choice (hi/en): ").strip().lower()

# ==================================================
# 7️⃣ REPORT SUMMARY
# ==================================================
if choice == "hi":
    summary = (
        f"यह रिपोर्ट {fields['DATE']} को {fields['TIME']} बजे दर्ज की गई है। "
        f"शिकायतकर्ता {fields['NAME']} द्वारा "
        f"{fields['INCIDENT_PLACE']} क्षेत्र में "
        f"{fields['COMPLAINT_TYPE']} से संबंधित शिकायत दर्ज की गई है।"
    )
else:
    summary = (
        f"This report was generated on {fields['DATE']} at {fields['TIME']}. "
        f"The complainant {fields['NAME']} reported a "
        f"{fields['COMPLAINT_TYPE']} near {fields['INCIDENT_PLACE']}."
    )

# ==================================================
# 8️⃣ FINAL REPORT (BILINGUAL)
# ==================================================
if choice == "hi":
    report = f"""
==================================================
            पुलिस शिकायत रिपोर्ट
==================================================
इनपुट भाषा        : {input_language}
AI पुष्टि ऑडियो     : उपयोग किया गया
रिपोर्ट भाषा       : हिंदी

--------------------------------------------------
1. रिपोर्ट सारांश
--------------------------------------------------
{summary}

--------------------------------------------------
2. शिकायत विवरण (हिंदी)
--------------------------------------------------
{hindi_text}

--------------------------------------------------
तैयार किया गया : Voice-Based FIR System
--------------------------------------------------
"""
else:
    report = f"""
==================================================
            POLICE COMPLAINT REPORT
==================================================
Input Language    : {input_language}
AI Confirmation  : Used
Report Language  : English

--------------------------------------------------
1. REPORT SUMMARY
--------------------------------------------------
{summary}

--------------------------------------------------
2. COMPLAINT DESCRIPTION (ENGLISH)
--------------------------------------------------
{english_text}

--------------------------------------------------
Generated By : Voice-Based FIR System
--------------------------------------------------
"""

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write(report)

print("\n📄 FINAL REPORT GENERATED → final_report.txt")
print("🎉 DONE — AI CONFIRMATION + FULL PIPELINE WORKING")
