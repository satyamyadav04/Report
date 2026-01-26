from faster_whisper import WhisperModel
import streamlit as st

@st.cache_resource
def load_fw_model():
    return WhisperModel(
        "small",
        device="cpu",
        compute_type="int8" 
    )

fw_model = load_fw_model()
