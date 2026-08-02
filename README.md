# Struktur Modular Streamlit

Jalankan aplikasi dari folder project:

```bash
streamlit run app.py
```

Struktur utama:

```text
streamlit_modular/
├── app.py
├── config.py
├── styles.py
├── model/
├── vector_store/
├── services/
│   ├── model_service.py
│   ├── preprocessing.py
│   ├── classification.py
│   ├── similarity.py
│   └── document_service.py
├── ui/
│   └── components.py
└── utils/
    └── helpers.py
```

Folder `model` dan `vector_store` dari project lama tetap diletakkan sejajar dengan `app.py`.
