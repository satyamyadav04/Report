# 🎙️ Voice-Based FIR Generation System (Hindi & English)

A **voice-driven police complaint (FIR) generation system** that converts user-recorded audio into **structured, editable, and legally formatted FIR reports** in **Hindi or English**, using **AI-based speech-to-text** and rule-based information extraction.

The system is optimized for **Indian accents**, **offline usage**, and **hackathon / production environments**.

---

## Key Features

- 🎧 Audio-to-text transcription (Hindi optimized)
- 🇮🇳 Strong support for Hindi, Hinglish, and English
- ⚡ Ultra-fast transcription using `faster-whisper`
- 🔁 Hindi → English translation
- 🧠 Automatic FIR field extraction (Name, Place, Complaint Type, Date, Time)
- 📝 Editable & user-confirmed transcripts
- 📄 Final FIR report generation (language-based)
- 🔐 Audio Evidence ID generation
- 🧩 Fully offline after model download

---

## Tech Stack

- **Frontend / UI**: Streamlit
- **Speech-to-Text**: Whisper / faster-whisper
- **Language Processing**: Regex + Rule-based NLP
- **Audio Processing**: FFmpeg (recommended)
- **Language Support**: Hindi & English
- **Deployment**: Local / Hackathon-ready

---

## Project Structure

```text
├── app.py                     # Streamlit main app
├── model.py                   # Whisper model loader (cached)
├── transcription.py           # Transcription pipelines
├── extraction.py              # FIR field extraction logic
├── report_generator.py        # Summary & final FIR report
├── utils.py                   # Helpers (Audio ID, validation)
├── requirements.txt
├── README.md
└── models/                    # Local Whisper models (optional)


---


## Installation & Setup

# Clone Repository
```

git clone https://github.com/your-username/voice-based-fir-system.git
cd voice-based-fir-system

```

# Install Dependencies
```

venv\Scripts\activate
pip install -r requirements.txt

```

# Running the Application
```

streamlit run app.py
Open in -> http://localhost:8501

```

---


## FIR Generation Logic
# Input

- User-recorded audio (Hindi / English)

# Output

- Hindi Transcript
- English Translation
- Extracted FIR Fields
- Final FIR Report (based on input language)

# Sample FIR Output (Hindi)

```

पुलिस शिकायत रिपोर्ट

रिपोर्ट सारांश:
यह रिपोर्ट 26-01-2026 को 10:30 बजे दर्ज की गई है।
शिकायतकर्ता राहुल शर्मा द्वारा मेट्रो स्टेशन क्षेत्र में
चोरी से संबंधित शिकायत दर्ज की गई है।

```

---

# Audio Evidence ID

\*\*Each FIR is tagged with a unique ID:

```
AE-YYYYMMDD-HHMMSS
```
---
## Contribution

Pull requests are welcome.
For major changes, please open an issue first.