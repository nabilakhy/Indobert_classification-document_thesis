import faiss
import numpy as np


def search_similar_cases(
    text,
    predicted_label,
    embedding_model,
    index,
    metadata,
    top_k=3,
):
    if not metadata or index.ntotal == 0:
        return []

    query_embedding = embedding_model.encode([text], convert_to_numpy=True)
    query_embedding = np.asarray(query_embedding, dtype="float32")
    faiss.normalize_L2(query_embedding)

    search_k = min(top_k * 20, len(metadata), index.ntotal)
    scores, indices = index.search(query_embedding, search_k)

    same_label_results = []
    other_label_results = []

    for score, metadata_index in zip(scores[0], indices[0]):
        if metadata_index == -1 or metadata_index >= len(metadata):
            continue

        item = metadata[metadata_index]
        item_label = str(item.get("label", "-"))
        case = {
            "filename": str(item.get("filename", "Dokumen referensi")),
            "label": item_label,
            "similarity_score": float(score),
            "text_preview": str(item.get("text", ""))[:1000],
            "same_label": item_label == str(predicted_label),
        }

        if case["same_label"]:
            same_label_results.append(case)
        else:
            other_label_results.append(case)

    same_label_results.sort(
        key=lambda item: item["similarity_score"], reverse=True
    )
    other_label_results.sort(
        key=lambda item: item["similarity_score"], reverse=True
    )

    final_results = same_label_results[:top_k]
    remaining = top_k - len(final_results)

    if remaining > 0:
        final_results.extend(other_label_results[:remaining])

    return final_results
