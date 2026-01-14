from field_extractor import extract_report_fields
from report_generator import (
    generate_report_summary,
    generate_final_report
)

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
    hindi_text,
    english_text,
    report_language,
    # audio_evidence_id,
    input_language
):
    summary = generate_report_summary(fields, report_language)
    report = generate_final_report(
        fields=fields,
        summary=summary,
        report_language=report_language,
        hindi_text=hindi_text,
        english_text=english_text,
        # audio_evidence_id=audio_evidence_id,
        input_language=input_language
    )

    return report
