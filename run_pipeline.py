import subprocess
from voice_video.pdf_generator import generate_pdf

# 1️⃣ Run existing pipeline
subprocess.run(["python", "voice-video/transcribe.py"])

# 2️⃣ Read generated report
with open("final_report.txt", "r", encoding="utf-8") as f:
    report_text = f.read()

# 3️⃣ Generate PDF
generate_pdf(report_text)

print("✅ PDF FIR Generated → final_report.pdf")