import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Voice FIR System", layout="centered")
st.title("🎙️ Voice‑Based FIR Generation System")

# Button to generate FIR
if st.button("▶️ Generate FIR"):
    with st.spinner("Processing..."):
        subprocess.run(["python", "run_pipeline.py"])
    st.success("✅ FIR Generated Successfully")

# ✅ SAFE CHECK before showing download button
if os.path.exists("final_report.pdf"):
    with open("final_report.pdf", "rb") as f:
        st.download_button(
            label="📄 Download FIR PDF",
            data=f,
            file_name="FIR_Report.pdf",
            mime="application/pdf"
        )
else:
    st.info("ℹ️ FIR PDF will appear here after generation.")
