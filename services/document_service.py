import os

from config import FAISS_INDEX_PATH, METADATA_PATH, TOP_K_SIMILAR
from services.classification import predict_document
from services.model_service import (
    load_classification_model,
    load_embedding_model,
    load_faiss_index,
)
from services.preprocessing import chunk_text, clean_text, extract_text_from_pdf
from services.similarity import search_similar_cases


def process_uploaded_document(uploaded_file):
    tokenizer, model, id_to_label = load_classification_model()

    raw_text, total_pages = extract_text_from_pdf(uploaded_file)
    cleaned_text = clean_text(raw_text)

    if not cleaned_text.split():
        raise ValueError(
            "Teks tidak berhasil diekstraksi. Gunakan PDF yang berisi teks digital, bukan hanya hasil scan gambar."
        )

    chunks = chunk_text(cleaned_text)
    final_label, avg_confidence, result_df, label_distribution = predict_document(
        chunks,
        tokenizer,
        model,
        id_to_label,
    )

    faiss_ready = False
    similar_cases = []

    if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(METADATA_PATH):
        embedding_model = load_embedding_model()
        faiss_index, metadata = load_faiss_index()
        similar_cases = search_similar_cases(
            cleaned_text,
            final_label,
            embedding_model,
            faiss_index,
            metadata,
            top_k=TOP_K_SIMILAR,
        )
        faiss_ready = True

    return {
        "final_label": final_label,
        "avg_confidence": avg_confidence,
        "result_df": result_df,
        "label_distribution": label_distribution,
        "similar_cases": similar_cases,
        "faiss_ready": faiss_ready,
        "cleaned_text": cleaned_text,
        "chunks": chunks,
        "total_pages": total_pages,
        "total_words": len(cleaned_text.split()),
        "total_chunks": len(chunks),
        "file_name": uploaded_file.name,
        "file_size_kb": uploaded_file.size / 1024,
    }
