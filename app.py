import streamlit as st
import os
from voice_video.transcribe import transcribe_hi_en
from run_pipeline import run_pipeline, generate_fir_report

from voice_video.record import record_audio_video
# Get the directory of this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_FILE = os.path.join(SCRIPT_DIR, "voice.wav")

st.set_page_config(page_title="AI FIR System", layout="wide")
st.title("🎙️ AI Voice-Based FIR System (Web Mode)")

# ---------------------------
# Upload Section
# ---------------------------
st.header("Step 1️⃣ Record your voice and video")

if st.button("🎥 Start Recording Audio & Video"):
    audio_file, video_file = record_audio_video()
    st.session_state["audio_file"] = audio_file
    st.session_state["video_file"] = video_file
    st.success("✅ Recording completed")    

st.session_state['audio_file'] = './voice.wav'  # For testing purposes

if st.session_state.get("audio_file") and st.button("▶️ Start Transcription"):

    audio_path = st.session_state["audio_file"]

    # ✅ Validate audio
    if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
        st.error("❌ Error: Audio file is empty or invalid. Please upload a valid audio file.")
    else:
        try:
            with st.spinner("Processing audio..."):
                texts = transcribe_hi_en(audio_path)   # 🔥 single call

            # ✅ Save to session state
            st.session_state["hindi"] = texts["hindi"]
            st.session_state["english"] = texts["english"]

            st.success("✅ Transcription completed")

        except Exception as e:
            st.error(f"❌ Transcription failed: {e}")


# ---------------------------
# Language Edit
# ---------------------------

if "hindi" in st.session_state:
    st.header("Step 2️⃣ Edit FIR")

    language = st.radio("Choose language", ["Hindi", "English"])

    text_map = {
        "Hindi": st.session_state["hindi"],
        "English": st.session_state["english"]
    }

    edited_text = st.text_area(
        f"Edit {language} FIR",
        value=text_map[language],
        height=300
    )

    if st.button("💾 Save Edited FIR"):
        filename = "hindi_text.txt" if language == "Hindi" else "english_text.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(edited_text)
        st.session_state["final_text"] = edited_text
        st.session_state["selected_language"] = "hi" if language == "Hindi" else "en"

        st.success("✅ FIR saved successfully")

# ---------------------------
# field extraction and report generation
# ---------------------------

if st.button("📄 Generate Report"):
    result = run_pipeline(
        audio_file="voice.wav",
        final_text=st.session_state["final_text"],
        language=st.session_state["selected_language"]
    )
    st.session_state["extracted_fields"] = result["extracted_fields"]
    st.subheader("📌 Extracted Fields")
    st.json(result["extracted_fields"])


if st.button("📄 Generate Final FIR Report"):
    final_report = generate_fir_report(
        fields=st.session_state["extracted_fields"],
        final_text=st.session_state["final_text"],
        input_language=st.session_state["selected_language"]
    )

    st.subheader("📄 Final Report Preview")
    st.text(final_report)

    st.download_button(
        "⬇️ Download Report",
        final_report,
        file_name="final_report.txt"
    )

st.markdown("---")
st.markdown("Developed by AI FIR System Team")
