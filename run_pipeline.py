from field_extractor import extract_report_fields
from report_generator import (
    generate_report_summary,
    generate_final_report
)
from voice_video.transcribe import generate_audio_evidence_id
def run_pipeline(audio_file, final_text, language):
    """
    Final AI pipeline
    """
    fields = extract_report_fields(
        text=final_text,
        language=language
    )
    return {
        "language": language,
        "final_text": final_text,
        "extracted_fields": fields
    }
    
def generate_fir_report(
    fields,
    final_text,
    input_language
    # report_language,
    # audio_evidence_id,
):
    summary = generate_report_summary(fields, input_language)
    report = generate_final_report(
        fields=fields,
        summary=summary,
        final_text=final_text,
        input_language=input_language,
        audio_evidence_id=generate_audio_evidence_id()
    )
    return report
