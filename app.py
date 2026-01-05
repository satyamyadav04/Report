import streamlit as st
import subprocess
import os

st.set_page_config(page_title="AI FIR System", layout="wide")
st.title("🎙️ AI Voice & Video FIR System")

# ===============================
# STEP 1: VIDEO UPLOAD
# ===============================
st.header("1️⃣ Upload Video (with Audio)")

video_file = st.file_uploader(
    "Upload recorded video (camera + mic)",
    type=["mp4", "webm"]
)

if video_file:
    with open("temp/input_video.mp4", "wb") as f:
        f.write(video_file.read())

    st.video("temp/input_video.mp4")
    st.success("Video uploaded successfully")

# ===============================
# STEP 2: EXTRACT AUDIO
# ===============================
st.header("2️⃣ Extract Audio from Video")

if st.button("🎧 Extract Audio"):
    subprocess.run([
        "ffmpeg", "-y",
        "-i", "temp/input_video.mp4",
        "-q:a", "0",
        "-map", "a",
        "temp/voice.wav"
    ])
    st.success("Audio extracted")
    st.audio("temp/voice.wav")

# ===============================
# STEP 3: AI CONFIRMATION VOICE
# ===============================
st.header("3️⃣ AI Confirmation Voice")

if st.button("🔊 Generate AI Voice"):
    subprocess.run(["python", "voice_video/transcribe.py"])
    st.success("AI confirmation voice generated")

if os.path.exists("ai_confirm.mp3"):
    st.audio("ai_confirm.mp3")

# ===============================
# STEP 4: REVIEW & EDIT TEXT
# ===============================
st.header("4️⃣ Review & Edit Text")

if os.path.exists("hindi_text.txt"):
    with open("hindi_text.txt", "r", encoding="utf-8") as f:
        edited = st.text_area(
            "Hindi Complaint (Editable)",
            f.read(),
            height=250
        )

    if st.button("💾 Save Edited Text"):
        with open("hindi_text.txt", "w", encoding="utf-8") as f:
            f.write(edited)
        st.success("Text updated")

# ===============================
# STEP 5: FINAL REPORT OPTIONS
# ===============================
st.header("5️⃣ Final Report Options")

format_choice = st.radio(
    "Choose final report format",
    ["TXT", "HTML (Save as PDF)"]
)

if st.button("📄 Generate Final Report"):
    subprocess.run(["python", "run_pipeline.py"])
    st.success("Final report generated")

# ===============================
# STEP 6: DOWNLOAD
# ===============================
st.header("6️⃣ Download")

if format_choice == "TXT" and os.path.exists("final_report.txt"):
    with open("final_report.txt", "r", encoding="utf-8") as f:
        st.download_button(
            "⬇️ Download TXT",
            f.read(),
            "FIR_Report.txt"
        )

if format_choice.startswith("HTML") and os.path.exists("final_report.html"):
    with open("final_report.html", "r", encoding="utf-8") as f:
        st.download_button(
            "⬇️ Download HTML (Print → PDF)",
            f.read(),
            "FIR_Report.html",
            mime="text/html"
        )
