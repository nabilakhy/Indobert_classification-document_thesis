import html
import re


def safe_text(value):
    return html.escape(str(value))


def score_to_percent(score):
    return max(0.0, min(float(score) * 100, 100.0))


def format_case_name(filename):
    clean = str(filename).replace(".xml", "")
    if re.fullmatch(r"[a-f0-9]{32}", clean):
        return f"\U0001f4c4 Dokumen Putusan #{clean[:8].upper()}"
    return html.escape(clean)
