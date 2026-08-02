import re

import fitz

from config import CHUNK_OVERLAP, CHUNK_SIZE


def extract_text_from_pdf(uploaded_file):
    uploaded_file.seek(0)
    text = ""

    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as document:
        total_pages = len(document)
        for page in document:
            text += page.get_text("text")

    return text, total_pages


def clean_text(text):
    text = text.lower()
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9\s.,;:()/-]", " ", text)
    return text.strip()


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))

        if end >= len(words):
            break

        start = end - overlap

    return chunks
