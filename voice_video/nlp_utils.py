import re
from datetime import datetime, timedelta

def extract_date_time(text):
    today = datetime.now()
    date = "Not Mentioned"
    time = "Not Mentioned"

    if "आज" in text:
        date = today.strftime("%d-%m-%Y")
    elif "कल" in text:
        date = (today - timedelta(days=1)).strftime("%d-%m-%Y")
    elif "परसों" in text:
        date = (today - timedelta(days=2)).strftime("%d-%m-%Y")

    t = re.search(r"(\d{1,2})\s*बजे", text)
    if t:
        time = f"{t.group(1)}:00"
    elif "रात" in text:
        time = "Night"
    elif "सुबह" in text:
        time = "Morning"
    elif "शाम" in text:
        time = "Evening"

    return date, time


def extract_place(text):
    places = [
        "रेलवे स्टेशन", "बस स्टैंड", "मेट्रो स्टेशन",
        "थाना", "बाज़ार", "मार्केट", "पार्क", "मॉल"
    ]
    for p in places:
        if p in text:
            return p
    return "Not Mentioned"