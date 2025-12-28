import cv2
import sounddevice as sd
from scipy.io.wavfile import write
import threading
import time

# ======================
# SETTINGS
# ======================
SAMPLE_RATE = 44100   # Audio quality
DURATION = 50         # Recording time (seconds)

# ======================
# AUDIO RECORDING
# ======================
def record_audio():
    print("🎙️ Audio recording started...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE),
                   samplerate=SAMPLE_RATE,
                   channels=1)
    sd.wait()
    write("voice.wav", SAMPLE_RATE, audio)
    print("✅ Audio saved as voice.wav")

# ======================
# VIDEO RECORDING
# ====================== 
def record_video():
    print("🎥 Video recording started...")
    cap = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(
        "video.avi",
        fourcc,
        20.0,
        (640, 480)
    )

    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        out.write(frame)
        cv2.imshow("Recording (Press Q to stop)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if time.time() - start_time >= DURATION:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("✅ Video saved as video.avi")

# ======================
# RUN BOTH TOGETHER     
# ======================
audio_thread = threading.Thread(target=record_audio)
video_thread = threading.Thread(target=record_video)

audio_thread.start()
video_thread.start()

audio_thread.join()
video_thread.join()

print("🎉 Audio + Video recording completed successfully!")