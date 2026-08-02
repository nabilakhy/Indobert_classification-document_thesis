import os
import xml.etree.ElementTree as ET
import pandas as pd
from tqdm import tqdm

dataset_dir = "./dataset"
records = []

# List tag yang ingin diambil supaya tidak panggil fungsi berulang
tags_to_find = ["fakta", "pertimbangan_hukum", "riwayat_dakwaan", "amar_putusan"]

files = [f for f in os.listdir(dataset_dir) if f.endswith(".xml")]

for filename in tqdm(files, desc="Progress Parsing"):
    filepath = os.path.join(dataset_dir, filename)
    try:
        # Gunakan iterparse jika file XML sangat besar (Opsional, tapi parse biasa cukup jika memori aman)
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Ambil data dasar
        data = {
            "filename": filename,
            "klasifikasi": root.attrib.get("klasifikasi", "").strip(),
            "sub_klasifikasi": root.attrib.get("sub_klasifikasi", "").strip()
        }

        # Ambil teks tiap tag secara efisien
        for tag in tags_to_find:
            el = root.find(tag)
            data[tag] = el.text.strip() if el is not None and el.text else ""

        records.append(data)

    except Exception as e:
        print(f"\nError pada {filename}: {e}")

# Buat DataFrame
if records:
    df = pd.DataFrame(records)
    # Gunakan compression='zip' kalau filenya terlalu besar untuk menghemat disk
    df.to_csv("dataset_pidana.csv", index=False, encoding="utf-8-sig")
    
    print(f"\n--- Selesai! ---")
    print(f"Total: {len(df)} dokumen berhasil diproses")
    print("\nTop 15 Sub-Klasifikasi:")
    print(df["sub_klasifikasi"].value_counts().head(15))
else:
    print("Tidak ada data yang berhasil diproses.")