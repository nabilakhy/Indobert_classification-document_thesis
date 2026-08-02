import streamlit as st

from services.llm_service import explain_classification
from services.document_service import process_uploaded_document
from styles import apply_custom_css
from ui.components import (
    render_classification_result,
    render_document_details,
    render_extracted_text,
    render_information_section,
    render_page_header,
    render_sidebar,
    render_similar_cases,
)


st.set_page_config(
    page_title="Klasifikasi Putusan Pidana",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def initialize_session_state():
    defaults = {
    "analysis_result": None,
    "processed_file_name": None,
    }

    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default


def main():
    initialize_session_state()
    apply_custom_css()

    render_sidebar()
    render_page_header()

    uploaded_file = st.file_uploader(
        "Tarik dan letakkan file PDF di sini, atau klik untuk memilih",
        type=["pdf"],
        accept_multiple_files=False,
        key="putusan_pdf_uploader",
    )

    _, button_column, _ = st.columns([1.1, 1, 1.1])

    with button_column:
        process_clicked = st.button(
            "⚙️ Proses Dokumen",
            type="primary",
            disabled=uploaded_file is None,
        )

    current_result = st.session_state.analysis_result

    # Menghilangkan hasil lama apabila pengguna memilih file baru
    if (
        uploaded_file is not None
        and st.session_state.processed_file_name is not None
        and uploaded_file.name != st.session_state.processed_file_name
    ):
        current_result = None

    if process_clicked and uploaded_file is not None:
        try:
            with st.spinner("Sedang memuat model dan memproses dokumen..."):
                result = process_uploaded_document(uploaded_file)

            st.session_state.analysis_result = result
            st.session_state.processed_file_name = uploaded_file.name

            current_result = result

            st.success("Dokumen berhasil diproses.")

        except Exception as error:
            st.error(f"Dokumen gagal diproses: {error}")
            st.exception(error)
            current_result = None

        if current_result is not None:
            render_classification_result(current_result)

        st.divider()
    
        with st.spinner("OpenAI sedang menjelaskan hasil klasifikasi..."):
            try:
                explanation = explain_classification(
                    label=current_result["final_label"],
                    confidence=current_result["avg_confidence"],
                    document_text=current_result["cleaned_text"],
                )

                st.markdown(explanation)

            except Exception as error:
                st.error(f"Gemini gagal membuat penjelasan: {error}")

        render_similar_cases(
            current_result["similar_cases"],
            current_result["faiss_ready"],
        )

        render_document_details(current_result)
        render_extracted_text(current_result)

    else:
        st.markdown(
            """
            <div class="empty-state">
                Unggah satu file PDF untuk memulai proses klasifikasi.
            </div>
            """,
            unsafe_allow_html=True,
        )

        render_information_section()

    st.markdown(
        """
        <div class="footer-note">
            Prototype Aplikasi Streamlit Klasifikasi Putusan Pidana
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()