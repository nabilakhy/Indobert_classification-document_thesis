import streamlit as st

from config import DARK, LIGHT, PRIMARY, TEXT


def apply_custom_css():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: #FFFFFF;
            color: #111827;
        }}

        header[data-testid="stHeader"] {{
            background: transparent;
        }}

        #MainMenu,
        footer {{
            visibility: hidden;
        }}

        .block-container {{
            max-width: 1120px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }}

        /* =========================
           SIDEBAR
        ========================= */

        section[data-testid="stSidebar"] {{
            background: #F3F6FA;
            border-right: 1px solid #C8CFD9;
            min-width: 290px !important;
            max-width: 290px !important;
        }}

        section[data-testid="stSidebar"] > div {{
            padding-top: 2rem;
        }}

        .sidebar-title {{
            color: {TEXT};
            font-size: 20px;
            font-weight: 800;
            margin: 4px 0 12px;
        }}

        .sidebar-subtitle {{
            color: {TEXT};
            font-size: 16px;
            font-weight: 800;
            margin: 12px 0 10px;
        }}

        .sidebar-copy {{
            color: #394150;
            font-size: 14px;
            line-height: 1.45;
            margin-bottom: 12px;
        }}

        .sidebar-divider {{
            height: 1px;
            background: #C8CFD9;
            margin: 14px 0;
        }}

        .history-item {{
            background: #FFFFFF;
            border: 1px solid #D0D5DD;
            border-radius: 8px;
            color: #737A87;
            font-size: 13px;
            padding: 12px 13px;
            margin-bottom: 8px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}

        .history-empty {{
            color: #8A93A3;
            font-size: 13px;
            font-style: italic;
        }}

        /* =========================
           HEADER
        ========================= */

        .page-header {{
            text-align: center;
            margin: 4px auto 26px;
        }}

        .page-title {{
            color: {TEXT};
            font-size: clamp(30px, 3vw, 42px);
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 8px;
        }}

        .page-subtitle {{
            color: #5C6270;
            font-size: 17px;
            line-height: 1.45;
            max-width: 720px;
            margin: auto;
        }}

        /* =========================
        FILE UPLOADER
        ========================= */

        div[data-testid="stFileUploader"] {{
            width: 100%;
        }}

        /* Area dropzone */
        div[data-testid="stFileUploader"] section {{
            min-height: 155px;
            background: #FBFCFF !important;
            border: 2px dashed {PRIMARY} !important;
            border-radius: 15px !important;
            padding: 30px 24px !important;
            display: flex !important;
            align-items: center !important;
        }}

        div[data-testid="stFileUploader"] section:hover {{
            background: #F4F8FF !important;
            border-color: {DARK} !important;
        }}

        /* Wrapper isi uploader */
        div[data-testid="stFileUploader"] section > div {{
            width: 100% !important;
            display: flex !important;
            align-items: center !important;
            gap: 18px !important;
        }}

        /* Wrapper instruksi dan info file */
        div[data-testid="stFileUploader"]
        [data-testid="stFileUploaderDropzoneInstructions"] {{
            display: flex !important;
            align-items: center !important;
            gap: 18px !important;
            margin: 0 !important;
        }}

        /* Teks instruksi */
        div[data-testid="stFileUploader"]
        [data-testid="stFileUploaderDropzoneInstructions"] * {{
            color: #394150 !important;
        }}

        /* Tombol Upload */
        div[data-testid="stFileUploader"] button {{
            background: {PRIMARY} !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 6px !important;
            min-width: 190px !important;
            min-height: 40px !important;
            height: 40px !important;
            padding: 0 22px !important;
            margin: 0 !important;
            font-weight: 600 !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 8px !important;
            line-height: 1 !important;
        }}

        div[data-testid="stFileUploader"] button:hover {{
            background: {DARK} !important;
            color: #FFFFFF !important;
        }}

        /* Ikon tombol Upload */
        div[data-testid="stFileUploader"] button svg {{
            width: 16px !important;
            height: 16px !important;
            color: #FFFFFF !important;
            fill: none !important;
        }}

        div[data-testid="stFileUploader"] button svg path {{
            stroke: #FFFFFF !important;
        }}

        /* Teks 200MB per file • PDF */
        div[data-testid="stFileUploader"] small {{
            color: #7A8495 !important;
            margin: 0 !important;
            padding: 0 !important;
            align-self: center !important;
            line-height: 1.2 !important;
            white-space: nowrap !important;
        }}

        /* =========================
           BUTTON
        ========================= */

        div[data-testid="stButton"] > button:not([data-testid="stTooltipIcon"]) {{
            width: 100%;
            background: {PRIMARY};
            color: #FFFFFF;
            border: 1px solid {PRIMARY};
            border-radius: 9px;
            min-height: 52px;
            font-size: 17px;
            font-weight: 750;
        }}

        button[data-testid="stTooltipIcon"],
        div[data-testid="stTooltipIcon"] button {{
            width: auto !important;
            min-width: 0 !important;
            min-height: 0 !important;
            height: auto !important;
            padding: 0 !important;
            margin: 0 !important;

            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: #FFFFFF !important;
        }}

        button[data-testid="stTooltipIcon"] svg,
        div[data-testid="stTooltipIcon"] button svg {{
            width: 18px !important;
            height: 18px !important;
            color: #FFFFFF !important;
            fill: none !important;
        }}

        button[data-testid="stTooltipIcon"] svg path,
        div[data-testid="stTooltipIcon"] button svg path {{
            stroke: #FFFFFF !important;
        }}

        div[data-testid="stButton"] > button:not([data-testid="stTooltipIcon"]):hover {{
            background: {DARK};
            border-color: {DARK};
            color: #FFFFFF;
        }}

        div.stButton > button:focus {{
            color: #FFFFFF;
            border-color: {DARK};
            box-shadow: none;
        }}

        div[data-testid="stButton"] > button:not([data-testid="stTooltipIcon"]):disabled {{
            background: #A8B4C7;
            border-color: #A8B4C7;
            color: #F8FAFC;
        }}

        /* =========================
           CLASSIFICATION RESULT
        ========================= */

        .classification-card {{
            background: {LIGHT};
            border: 2px solid {PRIMARY};
            border-radius: 14px;
            padding: 20px 26px 18px;
            margin-top: 22px;
        }}

        .classification-title,
        .section-title {{
            color: {TEXT};
            font-size: 20px;
            font-weight: 800;
        }}

        .classification-title {{
            margin-bottom: 15px;
        }}

        .section-title {{
            margin: 28px 0 16px;
        }}

        .result-row {{
            display: grid;
            grid-template-columns: 220px minmax(250px, 1fr);
            align-items: center;
            gap: 16px;
            margin: 10px 0;
        }}

        .result-label {{
            color: #202735;
            font-size: 16px;
        }}

        .prediction-pill {{
            background: {PRIMARY};
            color: #FFFFFF;
            border-radius: 999px;
            padding: 8px 18px;
            text-align: center;
            font-size: 15px;
            font-weight: 750;
            overflow-wrap: anywhere;
        }}

        .confidence-wrap {{
            display: grid;
            grid-template-columns: minmax(180px, 1fr) 54px;
            align-items: center;
            gap: 12px;
        }}

        .progress-track {{
            height: 21px;
            border: 1.5px solid {PRIMARY};
            border-radius: 999px;
            background: #DCE7F7;
            overflow: hidden;
        }}

        .progress-fill {{
            height: 100%;
            background: {PRIMARY};
            border-radius: 999px;
        }}

        .progress-number {{
            color: {PRIMARY};
            font-size: 15px;
            white-space: nowrap;
        }}

        .note {{
            color: #7A8495;
            font-size: 13px;
            font-style: italic;
            margin-top: 16px;
        }}

        /* =========================
           SIMILAR CASE CARDS
        ========================= */

        .case-card {{
            height: 205px;
            border: 1px solid #C9CDD3;
            border-radius: 10px;
            background: #FFFFFF;
            padding: 14px 16px 12px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            margin-bottom: 8px;
        }}

        .case-title {{
            color: {TEXT};
            font-size: 14px;
            line-height: 1.35;
            font-weight: 800;
            margin-bottom: 9px;
            overflow-wrap: anywhere;
        }}

        .case-preview {{
            color: #5F6673;
            font-size: 13px;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        .case-score-row {{
            display: grid;
            grid-template-columns: minmax(100px, 1fr) 36px;
            align-items: center;
            gap: 8px;
            margin-top: 12px;
        }}

        .case-track {{
            height: 18px;
            background: #DCE7F7;
            border-radius: 999px;
            overflow: hidden;
        }}

        .case-fill {{
            height: 100%;
            background: {PRIMARY};
            border-radius: 999px;
        }}

        .case-percent {{
            color: {PRIMARY};
            font-size: 11px;
            text-align: right;
        }}

        /* =========================
           INFORMATION SECTION
        ========================= */

        .info-section {{
            margin-top: 42px;
            text-align: center;
        }}

        .info-eyebrow {{
            color: {PRIMARY};
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 1.2px;
            margin-bottom: 8px;
            text-transform: uppercase;
        }}

        .info-heading {{
            color: {TEXT};
            font-size: 25px;
            font-weight: 800;
            line-height: 1.25;
        }}

        .info-description {{
            color: #697386;
            font-size: 14px;
            line-height: 1.55;
            max-width: 680px;
            margin: 9px auto 22px;
        }}

        /* =========================
           ARTICLE CARDS
        ========================= */

        .article-card {{
            min-height: 190px;
            height: 100%;
            background: #FFFFFF;
            border: 1px solid #D8E0EC;
            border-radius: 14px;
            padding: 20px 18px;
            box-shadow: 0 6px 18px rgba(28, 55, 92, 0.06);
            margin-bottom: 10px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}

        .article-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 24px rgba(28, 55, 92, 0.10);
        }}

        .article-icon {{
            font-size: 28px;
            margin-bottom: 13px;
        }}

        .article-title {{
            color: {TEXT};
            font-size: 17px;
            font-weight: 800;
            margin-bottom: 8px;
        }}

        .article-summary {{
            color: #667085;
            font-size: 13px;
            line-height: 1.55;
        }}

        .article-link {{
            color: {PRIMARY};
            font-size: 13px;
            font-weight: 700;
            margin-top: 14px;
        }}

        /* =========================
           DISCLAIMER
        ========================= */

        .disclaimer-box {{
            margin-top: 22px;
            background: #F5F8FD;
            border: 1px solid #D7E0ED;
            border-left: 5px solid {PRIMARY};
            border-radius: 10px;
            padding: 16px 18px;
        }}

        .disclaimer-title {{
            color: {TEXT};
            font-size: 14px;
            font-weight: 800;
            margin-bottom: 4px;
        }}

        .disclaimer-text {{
            color: #667085;
            font-size: 13px;
            line-height: 1.5;
        }}

        /* =========================
           EMPTY STATE
        ========================= */

        .empty-state {{
            margin-top: 18px;
            padding: 16px 18px;
            border: 1px solid #D7DFEB;
            border-radius: 10px;
            background: #F8FAFD;
            color: #657084;
            text-align: center;
            font-size: 14px;
        }}

        /* =========================
           EXPANDER
        ========================= */

        div[data-testid="stExpander"] {{
            border: 1px solid #D5DAE2;
            border-radius: 10px;
            background: #FFFFFF;
        }}

        div[data-testid="stExpander"] details {{
            border-radius: 10px;
        }}

        div[data-testid="stExpander"] summary {{
            color: {TEXT};
            font-weight: 600;
        }}

        /* =========================
           DATAFRAME
        ========================= */

        div[data-testid="stDataFrame"] {{
            border: 1px solid #D5DAE2;
            border-radius: 10px;
            overflow: hidden;
        }}

        /* =========================
           TABS
        ========================= */

        button[data-baseweb="tab"] {{
            font-size: 14px;
            font-weight: 600;
        }}

        button[data-baseweb="tab"][aria-selected="true"] {{
            color: {PRIMARY};
        }}

        /* =========================
           SELECTBOX
        ========================= */

        div[data-baseweb="select"] > div {{
            border-radius: 8px;
            border-color: #D0D5DD;
        }}

        /* =========================
           FOOTER
        ========================= */

        .footer-note {{
            color: #9A9A9A;
            font-size: 12px;
            font-style: italic;
            text-align: center;
            margin-top: 80px;
        }}

        /* =========================
        CHUNK DETAIL
        ========================= */

        .chunk-card {{
            margin-top: 16px;
            background: #FFFFFF;
            border: 1px solid #D5DDEA;
            border-radius: 14px;
            padding: 20px;
            box-shadow: 0 5px 16px rgba(28, 55, 92, 0.05);
        }}

        .chunk-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            padding-bottom: 15px;
            border-bottom: 1px solid #E3E8F0;
        }}

        .chunk-title {{
            color: {TEXT};
            font-size: 18px;
            font-weight: 800;
        }}

        .chunk-subtitle {{
            color: #7A8495;
            font-size: 12px;
            margin-top: 3px;
        }}

        .chunk-badge {{
            background: {PRIMARY};
            color: #FFFFFF;
            border-radius: 999px;
            padding: 7px 14px;
            font-size: 12px;
            font-weight: 700;
            white-space: nowrap;
        }}

        .chunk-meta-grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 12px;
            margin: 16px 0;
        }}

        .chunk-meta-item {{
            background: #F5F8FD;
            border: 1px solid #DCE4F0;
            border-radius: 10px;
            padding: 12px 14px;
        }}

        .chunk-meta-label {{
            color: #7A8495;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}

        .chunk-meta-value {{
            color: {TEXT};
            font-size: 14px;
            font-weight: 750;
            overflow-wrap: anywhere;
        }}

        .chunk-content {{
            max-height: 320px;
            overflow-y: auto;
            background: #F8FAFD;
            border: 1px solid #DFE5EE;
            border-radius: 10px;
            padding: 16px 18px;
            color: #4F5968;
            font-size: 14px;
            line-height: 1.75;
            text-align: justify;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
        }}

        .chunk-content::-webkit-scrollbar {{
            width: 8px;
        }}

        .chunk-content::-webkit-scrollbar-track {{
            background: #EEF2F7;
            border-radius: 999px;
        }}

        .chunk-content::-webkit-scrollbar-thumb {{
            background: #B3C0D4;
            border-radius: 999px;
        }}

        /* =========================
           RESPONSIVE
        ========================= */

        @media (max-width: 800px) {{
            .block-container {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}

            .result-row {{
                grid-template-columns: 1fr;
                gap: 7px;
            }}

            .classification-card {{
                padding: 18px;
            }}

            .page-title {{
                font-size: 30px;
            }}

            .page-subtitle {{
                font-size: 15px;
            }}

            .article-card {{
                min-height: auto;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )