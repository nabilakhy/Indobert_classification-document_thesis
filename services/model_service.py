import pickle

import faiss
import pandas as pd
import streamlit as st

from huggingface_hub import close_session, hf_hub_download
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from config import (
    FAISS_INDEX_PATH,
    METADATA_PATH,
    MODEL_PATH,
)


EMBEDDING_MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


@st.cache_resource
def load_classification_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

    model.eval()

    label_mapping_path = hf_hub_download(
        repo_id=MODEL_PATH,
        filename="label_mapping.csv",
    )

    label_df = pd.read_csv(label_mapping_path)

    id_to_label = dict(
        zip(
            label_df["label_id"],
            label_df["label"],
        )
    )

    return tokenizer, model, id_to_label


@st.cache_resource
def load_embedding_model():
    # Memastikan client Hugging Face dibuat ulang
    close_session()

    return SentenceTransformer(
        EMBEDDING_MODEL_NAME,
        device="cpu",
    )


@st.cache_resource
def load_faiss_index():
    index = faiss.read_index(
        FAISS_INDEX_PATH
    )

    with open(METADATA_PATH, "rb") as file:
        metadata = pickle.load(file)

    return index, metadata