import streamlit as st

from textwrap import dedent

from utils.helpers import safe_text, score_to_percent


def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-title">Tentang Aplikasi</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-divider"></div>',
            unsafe_allow_html=True,
        )

        sidebar_html = (
            '<div class="sidebar-copy">'
            'Model: IndoBERT<br><br>'
            '(indobenchmark/<br>'
            'indobert-base-p1)<br><br>'
            '18 Kelas Jenis<br>'
            'Tindak Pidana'
            '</div>'
        )

        st.markdown(
            sidebar_html,
            unsafe_allow_html=True,
        )

def render_page_header():
    header_html = (
        '<div class="page-header">'
        '<div class="page-title">Klasifikasi Jenis Tindak Pidana</div>'
        '<div class="page-subtitle">'
        'Unggah dokumen putusan (PDF) untuk memperoleh klasifikasi otomatis<br>'
        'dan rekomendasi kasus serupa'
        '</div>'
        '</div>'
    )

    st.markdown(
        header_html,
        unsafe_allow_html=True,
    )

    upload_info_html = (
        '<div class="upload-info">'
        'Maksimal satu dokumen PDF untuk setiap proses klasifikasi.'
        '</div>'
    )

    st.markdown(
        upload_info_html,
        unsafe_allow_html=True,
    )


def render_classification_result(result):
    confidence_value = float(result.get("avg_confidence", 0.0))

    confidence_percent = max(
        0.0,
        min(confidence_value * 100, 100.0),
    )

    final_label = safe_text(
        result.get("final_label", "Label tidak tersedia")
    )

    classification_html = (
        '<div class="classification-card">'
        '<div class="classification-title">Hasil Klasifikasi</div>'

        '<div class="result-row">'
        '<div class="result-label">Jenis Tindak Pidana:</div>'
        f'<div class="prediction-pill">{final_label}</div>'
        '</div>'

        '<div class="result-row">'
        '<div class="result-label">Confidence Score:</div>'

        '<div class="confidence-wrap">'
        '<div class="progress-track">'
        f'<div class="progress-fill" style="width:{confidence_percent:.2f}%;"></div>'
        '</div>'

        f'<div class="progress-number">{confidence_percent:.2f}%</div>'
        '</div>'
        '</div>'

        '<div class="note">'
        'Hasil diperoleh dari agregasi prediksi seluruh chunk dokumen.'
        '</div>'

        '</div>'
    )

    st.markdown(
        classification_html,
        unsafe_allow_html=True,
    )


def render_similar_cases(similar_cases, faiss_ready):
    st.markdown(
        (
            '<div class="section-title">'
            'Kasus Serupa (Semantic Similarity Search)'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    if not faiss_ready:
        st.warning(
            "Fitur kasus serupa belum aktif karena FAISS index "
            "atau metadata belum tersedia."
        )
        return

    if not similar_cases:
        st.info("Belum ditemukan kasus serupa dari dokumen referensi.")
        return

    cases_to_display = similar_cases[:3]
    columns = st.columns(len(cases_to_display))

    for column, case in zip(columns, cases_to_display):
        similarity_score = float(case.get("similarity_score", 0.0))

        percent = max(
            0.0,
            min(score_to_percent(similarity_score), 100.0),
        )

        filename = safe_text(
            case.get("filename", "Dokumen tanpa nama")
        )

        preview_text = str(
            case.get("text_preview", "")
        ).strip()

        if not preview_text:
            preview_text = "Cuplikan teks tidak tersedia."

        preview = safe_text(preview_text)

        case_html = (
            '<div class="case-card">'
            '<div>'
            f'<div class="case-title">{filename}</div>'
            f'<div class="case-preview">...{preview}...</div>'
            '</div>'
            '<div class="case-score-row">'
            '<div class="case-track">'
            f'<div class="case-fill" style="width:{percent:.2f}%;"></div>'
            '</div>'
            f'<div class="case-percent">{percent:.0f}%</div>'
            '</div>'
            '</div>'
        )

        with column:
            st.markdown(
                case_html,
                unsafe_allow_html=True,
            )


def render_document_details(result):
    with st.expander(
        "Lihat informasi dan detail proses dokumen"
    ):
        info_columns = st.columns(4)

        info_columns[0].metric(
            "Jumlah Halaman",
            result.get("total_pages", 0),
        )

        info_columns[1].metric(
            "Jumlah Kata",
            result.get("total_words", 0),
        )

        info_columns[2].metric(
            "Jumlah Chunk",
            result.get("total_chunks", 0),
        )

        file_size_kb = float(
            result.get("file_size_kb", 0.0)
        )

        info_columns[3].metric(
            "Ukuran File",
            f"{file_size_kb:.1f} KB",
        )

        label_distribution = result.get(
            "label_distribution"
        )

        if label_distribution is not None:
            st.markdown(
                "**Distribusi Prediksi per Chunk**"
            )

            distribution_columns = st.columns([1, 2])

            with distribution_columns[0]:
                st.dataframe(
                    label_distribution,
                    width="stretch",
                    hide_index=True,
                )

            with distribution_columns[1]:
                if (
                    not label_distribution.empty
                    and "Label" in label_distribution.columns
                ):
                    st.bar_chart(
                        label_distribution.set_index("Label")
                    )

        result_df = result.get("result_df")

        if result_df is not None:
            st.markdown(
                "**Hasil Prediksi per Chunk**"
            )

            st.dataframe(
                result_df,
                width="stretch",
                hide_index=True,
            )


def render_extracted_text(result):
    with st.expander("Lihat teks hasil ekstraksi"):
        chunks = result.get("chunks", [])
        result_df = result.get("result_df")

        if not chunks:
            st.info("Teks hasil ekstraksi tidak tersedia.")
            return

        selected_index = st.selectbox(
            "Pilih chunk",
            options=range(len(chunks)),
            format_func=lambda index: f"Chunk {index + 1} dari {len(chunks)}",
            key="selected_extracted_chunk",
        )

        selected_chunk = chunks[selected_index]
        total_words = len(selected_chunk.split())

        predicted_label = "-"
        confidence_score = "-"

        if result_df is not None and not result_df.empty:
            if selected_index < len(result_df):
                selected_row = result_df.iloc[selected_index]

                predicted_label = safe_text(
                    selected_row.get("Label Prediksi", "-")
                )

                confidence_score = safe_text(
                    selected_row.get("Skor Kepercayaan", "-")
                )

        chunk_html = (
            '<div class="chunk-card">'
            '<div class="chunk-header">'
            '<div>'
            f'<div class="chunk-title">Chunk {selected_index + 1}</div>'
            f'<div class="chunk-subtitle">{total_words} kata</div>'
            '</div>'
            '<div class="chunk-badge">'
            f'{selected_index + 1} / {len(chunks)}'
            '</div>'
            '</div>'
            '<div class="chunk-meta-grid">'
            '<div class="chunk-meta-item">'
            '<div class="chunk-meta-label">Label Prediksi</div>'
            f'<div class="chunk-meta-value">{predicted_label}</div>'
            '</div>'
            '<div class="chunk-meta-item">'
            '<div class="chunk-meta-label">Confidence Score</div>'
            f'<div class="chunk-meta-value">{confidence_score}</div>'
            '</div>'
            '</div>'
            '<div class="chunk-content">'
            f'{safe_text(selected_chunk)}'
            '</div>'
            '</div>'
        )

        st.markdown(
            chunk_html,
            unsafe_allow_html=True,
        )


def render_information_section():
    information_header = (
        '<div class="info-section">'
        '<div class="info-eyebrow">INFORMASI SISTEM</div>'
        '<div class="info-heading">'
        'Kenali proses klasifikasi putusan pidana'
        '</div>'
        '<div class="info-description">'
        'Informasi singkat mengenai dokumen yang dapat diproses, '
        'tahapan analisis, serta cara membaca hasil yang ditampilkan oleh sistem.'
        '</div>'
        '</div>'
    )

    st.markdown(
        information_header,
        unsafe_allow_html=True,
    )

    articles = [
        {
            "icon": "📄",
            "title": "Dokumen yang Didukung",
            "summary": (
                "Gunakan putusan pengadilan berformat PDF "
                "yang mengandung teks digital."
            ),
            "body": (
                "Sistem menerima satu file PDF untuk setiap proses klasifikasi. "
                "PDF hasil pemindaian gambar mungkin tidak dapat diekstraksi "
                "dengan baik apabila belum melalui proses OCR."
            ),
        },
        {
            "icon": "🧠",
            "title": "Cara Sistem Bekerja",
            "summary": (
                "Teks diekstraksi, dibersihkan, dibagi menjadi chunk, "
                "lalu dianalisis menggunakan IndoBERT."
            ),
            "body": (
                "Setiap chunk diklasifikasikan secara terpisah. "
                "Label akhir diperoleh dari agregasi hasil prediksi seluruh chunk "
                "agar dokumen panjang tetap dapat dianalisis secara menyeluruh."
            ),
        },
        {
            "icon": "🔎",
            "title": "Kasus Serupa",
            "summary": (
                "FAISS mencari putusan referensi dengan konteks "
                "yang paling mendekati dokumen."
            ),
            "body": (
                "Skor kemiripan menunjukkan kedekatan semantik dengan dokumen "
                "referensi, bukan tingkat kesamaan hukum secara mutlak. "
                "Hasil tetap perlu ditinjau bersama isi putusan secara lengkap."
            ),
        },
    ]

    columns = st.columns(3)

    for index, (column, article) in enumerate(
        zip(columns, articles),
        start=1,
    ):
        article_icon = safe_text(article["icon"])
        article_title = safe_text(article["title"])
        article_summary = safe_text(article["summary"])

        article_html = (
            '<div class="article-card">'
            f'<div class="article-icon">{article_icon}</div>'
            f'<div class="article-title">{article_title}</div>'
            f'<div class="article-summary">{article_summary}</div>'
            '</div>'
        )

        with column:
            st.markdown(
                article_html,
                unsafe_allow_html=True,
            )

            with st.expander(
                "Baca selengkapnya",
                expanded=False,
            ):
                st.write(article["body"])

    disclaimer_html = (
        '<div class="disclaimer-box">'
        '<div class="disclaimer-title">Catatan penggunaan</div>'
        '<div class="disclaimer-text">'
        'Hasil klasifikasi dan rekomendasi kasus serupa digunakan sebagai '
        'dukungan analisis, bukan sebagai pengganti pertimbangan hukum atau '
        'pembacaan putusan secara menyeluruh.'
        '</div>'
        '</div>'
    )

    st.markdown(
        disclaimer_html,
        unsafe_allow_html=True,
    )