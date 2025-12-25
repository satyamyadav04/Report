import os
import re
from datetime import datetime
import whisper
from gtts import gTTS
from playsound import playsound

AUDIO_FILE = "voice.wav"          # human voice
AI_VOICE_FILE = "ai_hindi.mp3"    # AI generated Hindi voice
REPORT_FILE = "final_report.txt"

# ==================================================
# 🔥 FIR-SPECIFIC & DYNAMIC HINDI CORRECTION
# ==================================================
def fir_specific_dynamic_hindi_correction(text):
    text = re.sub(r"(.)\1{2,}", r"\1", text)

    corrections = {
        "दिल्लि": "दिल्ली",
        "हूई": "हुई",
        "गत्ना": "घटना",
        "इस्तल": "स्थल",
        "इस्तेशन": "स्टेशन",
        "रेल्वे": "रेलवे",
        "सिकायत": "शिकायत",
        "धर्निवाद": "धन्यवाद",
        "मवजूद": "मौजूद",
        "अनुरोद": "अनुरोध",
        "लगबक": "लगभग",
        "कल्व": "कल",
        "रंड": "रंग",
        "नीजी": "निजी"
    }

    for w, c in corrections.items():
        text = text.replace(w, c)

    fir_phrases = {
        "फोन चोरी हो गया": "मेरा मोबाइल फोन चोरी हो गया है",
        "फोन चोरी हुआ": "मेरा मोबाइल फोन चोरी हो गया है",
        "मेरी जानकारी": "फोन में मेरी निजी जानकारी मौजूद है",
        "शिकायत दर्ज": "मेरी शिकायत दर्ज की जाए",
    }

    for r, f in fir_phrases.items():
        text = text.replace(r, f)

    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s([।,])", r"\1", text)

    return text.strip()

# ==================================================
# 🔥 AUTO REPORT FIELD EXTRACTION (WITH INCIDENT PLACE)
# ==================================================
def extract_report_fields(hindi_text):
    fields = {}

    # Name
    name_match = re.search(r"मेरा नाम ([^ ]+ ?[^ ]*) है", hindi_text)
    fields["NAME"] = name_match.group(1) if name_match else "Not Mentioned"

    # City
    city_match = re.search(r"(दिल्ली|मुंबई|लखनऊ|पटना|कानपुर)", hindi_text)
    fields["PLACE"] = city_match.group(1) if city_match else "Not Mentioned"

    # 🔥 Incident Place (regex based)
    place_patterns = [
        r"रेलवे स्टेशन",
        r"बस स्टैंड",
        r"मेट्रो स्टेशन",
        r"बाज़ार",
        r"मार्केट",
        r"पार्क",
        r"मॉल",
        r"चौराहा",
        r"सड़क",
        r"थाना"
    ]

    incident_place = "Not Mentioned"
    for p in place_patterns:
        m = re.search(p, hindi_text)
        if m:
            incident_place = m.group(0)
            break

    fields["INCIDENT_PLACE"] = incident_place

    # Complaint Type
    if "चोरी" in hindi_text:
        fields["COMPLAINT_TYPE"] = "Mobile Theft Complaint"
    else:
        fields["COMPLAINT_TYPE"] = "General Complaint"

    now = datetime.now()
    fields["DATE"] = now.strftime("%d-%m-%Y")
    fields["TIME"] = now.strftime("%H:%M")

    return fields

# ==================================================
# 🔥 REPORT SUMMARY GENERATOR
# ==================================================
def generate_report_summary(fields):
    return (
        f"यह रिपोर्ट {fields['DATE']} को {fields['TIME']} बजे दर्ज की गई है। "
        f"शिकायतकर्ता {fields['NAME']} द्वारा "
        f"{fields['INCIDENT_PLACE']} क्षेत्र में "
        f"{fields['COMPLAINT_TYPE']} से संबंधित शिकायत दर्ज की गई है।"
    )

# ==================================================
# 1️⃣ LOAD WHISPER
# ==================================================
print("🧠 Loading Whisper (medium)...")
model = whisper.load_model("medium")

# ==================================================
# 2️⃣ HINDI TRANSCRIPTION
# ==================================================
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
hindi_text = fir_specific_dynamic_hindi_correction(hindi_text)

print("\n📄 FINAL HINDI TEXT:")
print(hindi_text)

with open("hindi_text.txt", "w", encoding="utf-8") as f:
    f.write(hindi_text)

# ==================================================
# 3️⃣ AI HINDI VOICE
# ==================================================
print("\n🔊 Generating AI Hindi Voice...")
tts = gTTS(text=hindi_text, lang="hi", tld="co.in")
tts.save(AI_VOICE_FILE)
playsound(AI_VOICE_FILE)

# ==================================================
# 4️⃣ ENGLISH TRANSLATION
# ==================================================
print("\n🌍 Translating to English...")

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

with open("english_text.txt", "w", encoding="utf-8") as f:
    f.write(english_text)

# ==================================================
# 5️⃣ ENHANCED AUTO REPORT GENERATION
# ==================================================
fields = extract_report_fields(hindi_text)
summary = generate_report_summary(fields)

report = f"""
==================================================
            POLICE COMPLAINT REPORT
        (AUTO-GENERATED BY AI SYSTEM)
==================================================

Report ID        : FIR-AUTO-001
Report Date      : {fields['DATE']}
Report Time      : {fields['TIME']}
Report Status    : Generated (Pending Verification)

--------------------------------------------------
1. REPORT SUMMARY
--------------------------------------------------
{summary}

--------------------------------------------------
2. COMPLAINANT DETAILS
--------------------------------------------------
Name             : {fields['NAME']}
City / Address   : {fields['PLACE']}
Contact Number   : Not Provided

--------------------------------------------------
3. INCIDENT DETAILS
--------------------------------------------------
Type of Complaint: {fields['COMPLAINT_TYPE']}
Place of Incident: {fields['INCIDENT_PLACE']}
Date of Incident : Not Mentioned
Time of Incident : Not Mentioned

--------------------------------------------------
4. COMPLAINT DESCRIPTION (HINDI)
--------------------------------------------------
{hindi_text}

--------------------------------------------------
5. COMPLAINT DESCRIPTION (ENGLISH)
--------------------------------------------------
{english_text}

--------------------------------------------------
6. SYSTEM ANALYSIS
--------------------------------------------------
• Input Mode          : Voice
• Language            : Hindi
• Correction Method   : FIR-Specific Dynamic Rules
• Translation         : AI-Based
• Report Generation   : Automatic

--------------------------------------------------
Generated By : Voice-Based FIR Generation System
--------------------------------------------------
(Signature of Complainant)
"""

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write(report)

print("\n📄 ENHANCED FINAL REPORT GENERATED → final_report.txt")
print("🎉 DONE — PROJECT FULLY COMPLETE")
