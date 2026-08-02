from collections import Counter

import numpy as np
import pandas as pd
import streamlit as st
import torch


def predict_document(chunks, tokenizer, model, id_to_label):
    predictions = []
    confidences = []
    label_names = []

    progress_bar = st.progress(0)
    status_text = st.empty()

    for index, chunk in enumerate(chunks):
        status_text.caption(
            f"Memproses bagian dokumen {index + 1} dari {len(chunks)}..."
        )

        inputs = tokenizer(
            chunk,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512,
        )

        with torch.no_grad():
            outputs = model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=1)
            confidence, prediction_id = torch.max(probabilities, dim=1)

        prediction_value = prediction_id.item()
        confidence_value = confidence.item()

        predictions.append(prediction_value)
        confidences.append(confidence_value)
        label_names.append(id_to_label[prediction_value])
        progress_bar.progress((index + 1) / len(chunks))

    progress_bar.empty()
    status_text.empty()

    counts = Counter(predictions)
    max_count = max(counts.values())
    candidates = [label_id for label_id, count in counts.items() if count == max_count]

    if len(candidates) == 1:
        final_prediction_id = candidates[0]
    else:
        final_prediction_id = max(
            candidates,
            key=lambda label_id: np.mean(
                [
                    score
                    for prediction, score in zip(predictions, confidences)
                    if prediction == label_id
                ]
            ),
        )

    selected_confidences = [
        score
        for prediction, score in zip(predictions, confidences)
        if prediction == final_prediction_id
    ]

    average_confidence = float(np.mean(selected_confidences))
    final_label = id_to_label[final_prediction_id]

    result_df = pd.DataFrame(
        {
            "Chunk ke-": range(1, len(predictions) + 1),
            "Label ID": predictions,
            "Label Prediksi": label_names,
            "Skor Kepercayaan": [f"{score:.2%}" for score in confidences],
        }
    )

    label_distribution = (
        result_df["Label Prediksi"]
        .value_counts()
        .rename_axis("Label")
        .reset_index(name="Jumlah Chunk")
    )

    return final_label, average_confidence, result_df, label_distribution
