import re
from datetime import datetime

def extract_report_fields(text: str, language: str = "hi"):
    """
    Extract structured FIR/report fields from user-approved text
    """
    fields = {}

    # =============================
    # NAME EXTRACTION
    # =============================
    fields["NAME"] = "Not Mentioned"

    if language == "hi":
        name_patterns = [
            r"मेरा नाम ([^,।]+)",
            r"नाम ([^,।]+)"
        ]
    else:
        name_patterns = [
            r"my name is ([^,.]+)",
            r"name is ([^,.]+)"
        ]

    for p in name_patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            fields["NAME"] = m.group(1).strip()
            break
        
    # =============================
    # CITY / PLACE
    # =============================
    cities = [
        "दिल्ली", "मुंबई", "लखनऊ", "पटना", "कानपुर",
        "Delhi", "Mumbai", "Lucknow", "Patna", "Kanpur"
    ]

    fields["PLACE"] = "Not Mentioned"
    for city in cities:
        if city.lower() in text.lower():
            fields["PLACE"] = city
            break

    # =============================
    # INCIDENT PLACE TYPE
    # =============================
    incident_places = [
        "रेलवे स्टेशन", "बस स्टैंड", "मेट्रो स्टेशन",
        "बाज़ार", "मार्केट", "पार्क", "मॉल", "थाना",
        "railway station", "bus stand", "metro station",
        "market", "park", "mall", "police station"
    ]

    fields["INCIDENT_PLACE"] = "Not Mentioned"
    for p in incident_places:
        if p.lower() in text.lower():
            fields["INCIDENT_PLACE"] = p
            break

    # =============================
    # COMPLAINT TYPE
    # =============================
    if any(word in text.lower() for word in ["चोरी", "steal", "theft", "stolen"]):
        fields["COMPLAINT_TYPE"] = "Theft Complaint"
    elif any(word in text.lower() for word in ["मारपीट", "assault", "fight"]):
        fields["COMPLAINT_TYPE"] = "Physical Assault"
    else:
        fields["COMPLAINT_TYPE"] = "General Complaint"

    # =============================
    # DATE & TIME
    # =============================
    now = datetime.now()
    fields["DATE"] = now.strftime("%d-%m-%Y")
    fields["TIME"] = now.strftime("%H:%M")

    return fields