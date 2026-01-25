import re
from datetime import datetime

def normalize(text: str):
    return re.sub(r"\s+", " ", text.lower().strip())

def extract_report_fields(text: str, language: str = "auto"):
    fields = {}
    text_norm = normalize(text)

    # =============================
    # NAME EXTRACTION (HI + EN + HINGLISH)
    # =============================
    fields["NAME"] = "Not Mentioned"

    name_patterns = [
        r"(?:मेरा नाम|मेरा नाम है|नाम है|नाम)\s+([a-zA-Z\u0900-\u097F ]{2,40})",
        r"(?:my name is|name is|i am)\s+([a-zA-Z ]{2,40})"
    ]

    for p in name_patterns:
        m = re.search(p, text_norm, re.IGNORECASE)
        if m:
            fields["NAME"] = m.group(1).strip().title()
            break

    # =============================
    # CITY / PLACE (Expandable)
    # =============================
    cities = {
        "delhi": "Delhi",
        "दिल्ली": "Delhi",
        "mumbai": "Mumbai",
        "मुंबई": "Mumbai",
        "lucknow": "Lucknow",
        "लखनऊ": "Lucknow",
        "patna": "Patna",
        "पटना": "Patna",
        "kanpur": "Kanpur",
        "कानपुर": "Kanpur"
    }

    fields["PLACE"] = "Not Mentioned"
    for key, value in cities.items():
        if key in text_norm:
            fields["PLACE"] = value
            break

    # =============================
    # INCIDENT PLACE TYPE
    # =============================
    incident_places = {
        "railway station": ["रेलवे स्टेशन", "station", "railway"],
        "bus stand": ["बस स्टैंड", "bus stand"],
        "metro station": ["मेट्रो स्टेशन", "metro"],
        "market": ["बाज़ार", "market", "bazaar"],
        "park": ["पार्क", "park"],
        "mall": ["मॉल", "mall"],
        "police station": ["थाना", "police station"]
    }

    fields["INCIDENT_PLACE"] = "Not Mentioned"
    for place, keywords in incident_places.items():
        if any(k in text_norm for k in keywords):
            fields["INCIDENT_PLACE"] = place.title()
            break

    # =============================
    # COMPLAINT TYPE (More Robust)
    # =============================
    complaint_map = {
        "Theft Complaint": ["चोरी", "चुरा", "steal", "stolen", "theft", "snatch"],
        "Physical Assault": ["मारपीट", "पीटा", "assault", "fight", "beaten"],
        "Harassment": ["छेड़छाड़", "harass", "molest", "threat"],
        "Lost Item": ["खो गया", "lost", "missing"]
    }

    fields["COMPLAINT_TYPE"] = "General Complaint"
    for ctype, keywords in complaint_map.items():
        if any(k in text_norm for k in keywords):
            fields["COMPLAINT_TYPE"] = ctype
            break

    # =============================
    # DATE EXTRACTION (Optional)
    # =============================
    date_match = re.search(
        r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", text_norm
    )

    if date_match:
        fields["DATE"] = date_match.group(1)
    else:
        fields["DATE"] = datetime.now().strftime("%d-%m-%Y")

    # =============================
    # TIME EXTRACTION (Optional)
    # =============================
    time_match = re.search(
        r"(\d{1,2}:\d{2})", text_norm
    )

    if time_match:
        fields["TIME"] = time_match.group(1)
    else:
        fields["TIME"] = datetime.now().strftime("%H:%M")

    return fields
