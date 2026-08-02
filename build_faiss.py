import os
import pickle
import faiss
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer


DATA_PATH = "data_referensi.csv"
VECTOR_DIR = "vector_store"
INDEX_PATH = os.path.join(VECTOR_DIR, "faiss_index.index")
METADATA_PATH = os.path.join(VECTOR_DIR, "metadata.pkl")


def main():
    os.makedirs(VECTOR_DIR, exist_ok=True)

    print("Membaca data_referensi.csv...")

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            "File data_referensi.csv tidak ditemukan. "
            "Pastikan file tersebut ada satu folder dengan build_faiss.py"
        )

    df = pd.read_csv(DATA_PATH)

    print("Kolom yang terbaca:")
    print(df.columns)
    print("Jumlah data awal:", len(df))

    required_columns = ["filename", "label", "clean_text"]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(
                f"Kolom '{col}' tidak ditemukan. "
                f"Kolom yang tersedia: {list(df.columns)}"
            )

    df = df.dropna(subset=["filename", "label", "clean_text"]).copy()

    df["filename"] = df["filename"].astype(str)
    df["label"] = df["label"].astype(str)
    df["clean_text"] = df["clean_text"].astype(str)

    print("Jumlah data setelah drop kosong:", len(df))
    print("Distribusi label:")
    print(df["label"].value_counts())

    print("Memuat model embedding...")
    embedding_model = SentenceTransformer(
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    print("Membuat embedding dokumen...")
    texts = df["clean_text"].tolist()

    embeddings = embedding_model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
        batch_size=32
    )

    embeddings = np.array(embeddings).astype("float32")

    # Normalisasi untuk cosine similarity
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    print("Membuat FAISS index...")
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    metadata = []

    for _, row in df.iterrows():
        metadata.append({
            "filename": row["filename"],
            "label": row["label"],
            "text": row["clean_text"]
        })

    print("Menyimpan FAISS index...")
    faiss.write_index(index, INDEX_PATH)

    print("Menyimpan metadata...")
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print("Selesai.")
    print("FAISS index disimpan di:", INDEX_PATH)
    print("Metadata disimpan di:", METADATA_PATH)


if __name__ == "__main__":
    main()