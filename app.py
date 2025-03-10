import sqlite3
from sqlite3 import Connection
import hashlib
import streamlit as st
import streamlit.components.v1 as components

# Tetapkan konfigurasi halaman
st.set_page_config(page_title="Aplikasi Penulisan Karangan", layout="wide")

# CSS untuk gaya tambahan (opsional)
st.markdown("""
<style>
    /* Gaya untuk ikon dengan warna latar belakang */
    .ikon-button {
        font-size: 24px;
        background: none;
        border: none;
        cursor: pointer;
        padding: 10px;
        margin: 5px;
        border-radius: 10px;
        transition: background-color 0.3s, color 0.3s;
    }
    .ikon-button:hover {
        opacity: 0.8;
    }

    /* Gaya untuk editor Quill */
    #editor-container {
        width: 100% !important;
        height: 400px !important;
    }
</style>
""", unsafe_allow_html=True)

# Warna & Ikon untuk Teknik Penulisan
teknik_info = {
    "Plot": {"ikon": "📖", "warna": "#000000", "tooltip": "Plot: Cerita utama atau rangka cerita."},
    "Imbasan Lalu": {"ikon": "⏳", "warna": "#FF7F50", "tooltip": "Imbasan Lalu: Kilas balik ke masa lalu."},
    "Imbasan Masa Depan": {"ikon": "🔮", "warna": "#800080", "tooltip": "Imbasan Masa Depan: Kilas ke masa depan."},
    "Gambaran": {"ikon": "🌄", "warna": "#008000", "tooltip": "Gambaran: Deskripsi visual yang jelas."},
    "KEPO": {"ikon": "🔍", "warna": "#FF4500", "tooltip": "KEPO: Menunjukkan rasa ingin tahu."},
    "BAYANG": {"ikon": "👀", "warna": "#B8860B", "tooltip": "BAYANG: Bayangan atau petunjuk halus."},
    "Saspen": {"ikon": "😱", "warna": "#808080", "tooltip": "Saspen: Menimbulkan
