def generate_pdf(report_text, filename="final_report.html"):
    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>FIR Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
            }}
            h1 {{
                text-align: center;
                text-transform: uppercase;
            }}
            pre {{
                white-space: pre-wrap;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <h1>Police Complaint Report</h1>
        <pre>{report_text}</pre>
    </body>
    </html>
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
