import whisper

# Load model once at module initialization
_model = None

def load_model(model_name="medium"):
    """Load model only once and cache it globally"""
    global _model
    if _model is None:
        _model = whisper.load_model(model_name)
    return _model

def get_model():
    """Get the already-loaded model without reloading"""
    global _model
    if _model is None:
        _model = whisper.load_model("medium")
    return _model

# Initialize model on import
_model = load_model()

# Print confirmation when script is run directly
if __name__ == "__main__":
    print("✓ Model loaded successfully!")
    print(f"Model: {_model}")
    print("You can now import get_model() from this module without reloading.")