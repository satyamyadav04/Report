# record.py
import cv2
import sounddevice as sd
from scipy.io.wavfile import write
import threading
import time

SAMPLE_RATE = 44100
DURATION = 50

def record_audio(output="voice.wav"):
    audio = sd.rec(int(DURATION * SAMPLE_RATE),
                   samplerate=SAMPLE_RATE,
                   channels=1)
    sd.wait()
    write(output, SAMPLE_RATE, audio)
    return output

def record_video(output="video.avi"):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output, fourcc, 20.0, (640, 480))

    start_time = time.time()
    while time.time() - start_time < DURATION:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()
    return output

def record_audio_video():
    t1 = threading.Thread(target=record_audio)
    t2 = threading.Thread(target=record_video)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    return "voice.wav", "video.avi"