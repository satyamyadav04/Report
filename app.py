import streamlit as st
import subprocess
import os

st.set_page_config(
    page_title="AI Voice FIR System",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ AI‑Based Voice FIR Generation System")
st.markdown("Generate police complaint reports from voice input using AI")

# ===============================
# SIDEBAR – OPTIONS
# ===============================
st.sidebar.header("⚙️ FIR Options")

report_lang = st.sidebar.radio(
    "Select Report Language",
    ["Hindi", "English"]
)

allow_edit = st.sidebar.checkbox(
    "Allow text editing before final report",
    value=True
)

st.sidebar.markdown("---")
st.sidebar.info("AI Confirmation Audio is always used")

# ===============================
# MAIN – VOICE INPUT
# ===============================
st.subheader("🎧 Step 1: Upload Voice Input")

uploaded_file = st.file_uploader(
    "Upload voice file (.wav)",
    type=["wav"]
)

if uploaded_file:
    with open("voice.wav", "wb") as f:
        f.write(uploaded_file.read())

    st.audio("voice.wav")
    st.success("Voice file uploaded successfully")

# ===============================
# GENERATE FIR BUTTON
# ===============================
st.subheader("🚀 Step 2: Generate FIR")

if st.button("▶️ Generate FIR from Voice"):
    if not os.path.exists("voice.wav"):
        st.error("Please upload a voice file first")
    else:
        with st.spinner("Processing voice and generating FIR..."):
            subprocess.run(["python", "run_pipeline.py"])
        st.success("FIR generated successfully")

# ===============================
# SHOW GENERATED CONTENT
# ===============================
st.subheader("📄 Step 3: Review Extracted Content")

if os.path.exists("hindi_text.txt"):
    st.markdown("### 📝 Hindi Text")
    with open("hindi_text.txt", "r", encoding="utf-8") as f:
        st.text_area(
            "Hindi Complaint",
            f.read(),
            height=200
        )

if os.path.exists("english_text.txt"):
    st.markdown("### 📝 English Text")
    with open("english_text.txt", "r", encoding="utf-8") as f:
        st.text_area(
            "English Complaint",
            f.read(),
            height=200
        )

# ===============================
# DOWNLOAD SECTION
# ===============================
st.subheader("⬇️ Download FIR")

if os.path.exists("final_report.txt"):
    with open("final_report.txt", "r", encoding="utf-8") as f:
        st.download_button(
            "📄 Download FIR (TXT)",
            data=f.read(),
            file_name="FIR_Report.txt"
        )

if os.path.exists("final_report.html"):
    with open("final_report.html", "r", encoding="utf-8") as f:
        st.download_button(
            "📕 Download FIR (HTML → Save as PDF)",
            data=f.read(),
            file_name="FIR_Report.html",
            mime="text/html"
        )

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.caption(
    "AI‑Based FIR System | Voice → Verification → Structured Report"
)