from voice_video.record import record_audio_video
from voice_video.transcribe import transcribe_pipline, confirmed_audio_to_text


def run_pipeline():
    voice_file, video_file = record_audio_video()
    print("starting transcribing pipeline...")
    original_text, input_language = transcribe_pipline(voice_file)
    
    print("generating AI confirmation audio...")
    hindi, english = confirmed_audio_to_text(voice_file)
    
    def save_language_files(texts: dict):
        with open("hindi_text.txt", "w", encoding="utf-8") as f:
            f.write(texts["hindi"])

        with open("english_text.txt", "w", encoding="utf-8") as f:
            f.write(texts["english"])
    save_language_files({"hindi": hindi, "english": english})
    
    