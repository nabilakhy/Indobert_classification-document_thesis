from openai import OpenAI
import streamlit as st


def explain_classification(label, confidence, document_text):

    if "DEEPSEEK_API_KEY" not in st.secrets:
        raise ValueError("DEEPSEEK_API_KEY belum dikonfigurasi.")

    client = OpenAI(
        api_key=st.secrets["DEEPSEEK_API_KEY"],
        base_url=st.secrets["DEEPSEEK_API_BASE"],
    )

    model = st.secrets["DEEPSEEK_MODEL"]

    confidence_percent = confidence * 100
    document_excerpt = document_text[:12000]

    system_prompt = """
Anda adalah asisten yang bertugas menjelaskan hasil
klasifikasi dokumen putusan pengadilan.

IndoBERT adalah model yang melakukan klasifikasi.
Anda tidak melakukan klasifikasi ulang.
Tugas Anda hanya menjelaskan hasil klasifikasi berdasarkan
informasi yang tersedia dalam dokumen.
"""

    user_prompt = f"""
HASIL KLASIFIKASI INDOBERT:

Jenis tindak pidana:
{label}

Tingkat keyakinan:
{confidence_percent:.2f}%

ISI DOKUMEN:
{document_excerpt}

ATURAN:
1. Jangan mengubah hasil klasifikasi IndoBERT.
2. Jangan mengubah nilai tingkat keyakinan.
3. Jangan melakukan klasifikasi ulang.
4. Jangan menambahkan fakta yang tidak terdapat dalam dokumen.
5. Gunakan bahasa Indonesia formal dan mudah dipahami.
6. Jelaskan hubungan antara isi dokumen dengan hasil klasifikasi.
7. Jangan memberikan nasihat hukum.
8. Buat penjelasan maksimal 2 paragraf.

Format:

### Penjelasan Hasil Klasifikasi

**Jenis Perkara:** {label}

**Tingkat Keyakinan:** {confidence_percent:.2f}%

**Penjelasan:**

Jelaskan secara singkat hubungan antara isi dokumen
dan hasil klasifikasi IndoBERT.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        timeout=60,
        max_tokens=512,
    )

    result = response.choices[0].message.content

    if not result:
        raise ValueError("LLM tidak menghasilkan penjelasan.")

    return result