import subprocess
from voice_video.pdf_generator import generate_pdf

# 1️⃣ Run main pipeline (unchanged)
subprocess.run(["python", "voice-video/transcribe.py"])


# 2️⃣ Read generated TXT report
with open("final_report.txt", "r", encoding="utf-8") as f:
    report_text = f.read()

# 3️⃣ Generate HTML FIR (PDF‑ready)
generate_pdf(report_text)

print("✅ FIR HTML generated → final_report.html")
