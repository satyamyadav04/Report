import whisper
import streamlit as st

@st.cache_resource
def load_model(model_name="small"):
    print("🔄 Loading Whisper model...")
    model = whisper.load_model(model_name)
    print("✅ Model loaded (local cache)")
    return model