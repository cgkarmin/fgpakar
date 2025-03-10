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
    "Saspen": {"ikon": "😱", "warna": "#808080", "tooltip": "Saspen: Menimbulkan rasa suspense."},
    "DEBAR": {"ikon": "💖", "warna": "#0ABAB5", "tooltip": "DEBAR: Menimbulkan rasa debaran."},
    "Dialog/Monolog": {"ikon": "🗣️", "warna": "#A52A2A", "tooltip": "Dialog/Monolog: Percakapan atau monolog."},
    "3 Dalam 1": {"ikon": "📜", "warna": "#8B4513", "tooltip": "3 Dalam 1: Tiga elemen dalam satu ayat."},
    "Peribahasa (PEMBACA)": {"ikon": "📝", "warna": "#00008B", "tooltip": "Peribahasa: Menggunakan peribahasa."},
    "DD2P": {"ikon": "📚", "warna": "#0C0C0C", "tooltip": "DD2P: Dua dalam dua perenggan."},
    "WAH": {"ikon": "🎭", "warna": "#4B0082", "tooltip": "WAH: Watak, Aksi, Huraian."},
    "PL": {"ikon": "🧠", "warna": "#8B008B", "tooltip": "PL: Pemikiran logik atau kreatif."},
}

# Simpan pemilihan teknik dalam `st.session_state`
if "selected_teknik" not in st.session_state:
    st.session_state.selected_teknik = "Plot"  # Default ke "Plot"
if "hasil_karangan_gabungan" not in st.session_state:
    st.session_state.hasil_karangan_gabungan = ""

# Fungsi untuk mengemas kini teknik yang dipilih
def pilih_teknik(teknik):
    st.session_state.selected_teknik = teknik
    st.query_params.update(selected_teknik=teknik)

# Semak parameter URL untuk mengemas kini teknik yang dipilih
query_params = st.query_params
if "selected_teknik" in query_params:
    st.session_state.selected_teknik = query_params["selected_teknik"]

# Fungsi untuk mendapatkan sambungan ke database
def get_connection() -> Connection:
    conn = sqlite3.connect('karangan.db')
    return conn

# Fungsi untuk membuat jadual pengguna
def create_user_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Fungsi untuk menyulitkan kata laluan
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Fungsi untuk mendaftar pengguna baru
def register_user(username: str, password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute('''
            INSERT INTO users (username, password) VALUES (?, ?)
        ''', (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Fungsi untuk mengesahkan pengguna
def validate_user(username: str, password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute('''
        SELECT * FROM users WHERE username = ? AND password = ?
    ''', (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Buat jadual pengguna jika belum wujud
create_user_table()

# Sidebar untuk Login/Daftar dan Buka Fail
with st.sidebar:
    st.title("Login/Daftar")
    username = st.text_input("Nama Pengguna")
    password = st.text_input("Kata Laluan", type="password")
    if st.button("Log Masuk"):
        if validate_user(username, password):
            st.success("Log masuk berjaya")
        else:
            st.error("Log masuk gagal")
    if st.button("Daftar"):
        if register_user(username, password):
            st.success("Pendaftaran berjaya")
        else:
            st.error("Pendaftaran gagal")

    st.title("Buka Fail")
    uploaded_file = st.file_uploader("Pilih fail karangan", type=["txt"])
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        st.session_state["file_content"] = content
    if "file_content" in st.session_state:
        st.text_area("Kandungan Fail", st.session_state["file_content"], height=200)

# Susunan Ikon Teknik dalam Satu Baris
st.subheader("🎨 Pilih Teknik Penulisan")
num_cols = 7  # Maksimum ikon dalam satu baris
ikon_keys = list(teknik_info.keys())

for i in range(0, len(ikon_keys), num_cols):
    cols = st.columns(num_cols)
    for j, col in enumerate(cols):
        if i + j < len(ikon_keys):
            teknik = ikon_keys[i + j]
            info = teknik_info[teknik]
            with col:
                # Gunakan butang Streamlit dengan on_click
                if st.button(
                    f"{info['ikon']}",
                    key=f"btn_{teknik}",
                    help=info["tooltip"],
                    on_click=pilih_teknik,  # Panggil fungsi pilih_teknik
                    args=(teknik,),  # Hantar argumen teknik
                ):
                    pass  # Tiada tindakan tambahan diperlukan

# Semak parameter URL untuk mengemas kini teknik yang dipilih
if "selected_teknik" in st.query_params:
    st.session_state.selected_teknik = st.query_params["selected_teknik"]

# Tata Letak Kolom
col1, col2 = st.columns([3, 1])  # Kolum kiri lebih lebar daripada kolum kanan

with col1:
    # Paparan Teknik yang Dipilih
    selected_teknik = st.session_state.selected_teknik
    warna_teknik = teknik_info[selected_teknik]["warna"]
    ikon_teknik = teknik_info[selected_teknik]["ikon"]

    st.markdown(
        f"<div style='text-align: center; padding: 10px; background-color: {warna_teknik}; "
        f"color: white; font-size: 20px; border-radius: 10px;'>"
        f"{ikon_teknik} {selected_teknik}</div>", unsafe_allow_html=True
    )

    # Fungsi untuk memaparkan editor Quill dengan keupayaan sembunyi/papar
    def rich_text_editor(label, key, expanded=True):
        if st.checkbox(f"Sembunyikan {label}", key=f"checkbox_{key}", value=expanded):
            st.subheader(label)
            components.html(f"""
            <!DOCTYPE html>
            <html>
            <head>
                <link href="https://cdn.quilljs.com/1.3.6/quill.snow.css" rel="stylesheet">
                <style>
                    #editor-container {{
                        width: 100% !important;
                        height: 400px !important; /* Tinggi editor */
                    }}
                    .ql-toolbar.ql-snow {{
                        display: flex;
                        justify-content: center;
                    }}
                    #status-{key} {{
                        color: green;
                        font-weight: bold;
                        margin-top: 10px;
                    }}
                </style>
            </head>
            <body>
                <div id="editor-container"></div>
                <script src="https://cdn.quilljs.com/1.3.6/quill.js"></script>
                <script>
                    var quill = new Quill('#editor-container', {{
                        theme: 'snow',
                        modules: {{
                            toolbar: [
                                ['bold', 'italic', 'underline'],
                                ['link', 'blockquote', 'code-block', 'image'],
                                ['ordered', 'bullet'],
                                ['sub', 'super'],
                                [{{ 'indent': '-1' }}, {{ 'indent': '+1' }}],
                                [{{ 'direction': 'rtl' }}],
                                [{{ 'size': ['small', false, 'large', 'huge'] }}],
                                [{{ 'color': [] }}, {{ 'background': [] }}],
                                [{{ 'align': [] }}],
                                ['clean']
                            ]
                        }}
                    }});

                    // Muatkan kandungan yang telah disimpan (jika ada)
                    var savedContent = '{st.session_state.get(f"quill_content-{key}", "")}';
                    if (savedContent) {{
                        quill.setContents(JSON.parse(savedContent));
                    }}

                    // Fungsi untuk menyimpan kandungan
                    function saveContent() {{
                        var content = quill.getContents(); // Simpan kandungan dalam format JSON
                        var hiddenInput = document.querySelector('input[name="quill_content-{key}"]');
                        hiddenInput.value = JSON.stringify(content);
                        // Paparkan makluman "Disimpan"
                        var statusDiv = document.querySelector('#status-{key}');
                        statusDiv.textContent = 'Disimpan';
                        setTimeout(function() {{
                            statusDiv.textContent = '';
                        }}, 2000); // Hilangkan makluman selepas 2 saat
                    }}

                    // Simpan kandungan secara automatik setiap 15 saat
                    setInterval(saveContent, 15000); // 15000 ms = 15 saat

                    // Simpan kandungan apabila butang "Simpan Perubahan" diklik
                    document.querySelector('button#save-btn-{key}').addEventListener('click', saveContent);
                </script>
                <form method="post">
                    <input type="hidden" name="quill_content-{key}" id="quill_content-{key}">
                    <button id="save-btn-{key}" type="submit">💾 Simpan Perubahan</button>
                </form>
                <div id="status-{key}"></div>
            </body>
            </html>
            """, height=450)  # Tinggi kontena editor

            # Simpan Perubahan
            if st.session_state.get(f"quill_content-{key}", ""):
                st.session_state[f"hasil_karangan_{key}"] = st.session_state.get(f"quill_content-{key}", "")

            # Paparkan hasil karangan yang disimpan
            if f"hasil_karangan_{key}" in st.session_state:
                components.html(f"""
                <link href="https://cdn.quilljs.com/1.3.6/quill.snow.css" rel="stylesheet">
                <div id="editor-container-display-{key}"></div>
                <script src="https://cdn.quilljs.com/1.3.6/quill.js"></script>
                <script>
                    var quill = new Quill('#editor-container-display-{key}', {{
                        theme: 'snow',
                        modules: {{
                            toolbar: false  // Sembunyikan toolbar pada paparan
                        }},
                        readOnly: true
                    }});
                    quill.setContents(JSON.parse('{st.session_state[f"hasil_karangan_{key}"]}'));
                </script>
                """)

    # Paparan bahagian-bahagian cerita dengan editor Quill (dibuka secara lalai)
    rich_text_editor("Permulaan", "permulaan")
    rich_text_editor("Sub-Konflik", "sub_konflik")
    rich_text_editor("Konflik", "konflik")
    rich_text_editor("Sub-Kemuncak", "sub_kemuncak")
    rich_text_editor("Kemuncak", "kemuncak")
    rich_text_editor("Peleraian", "peleraian")
    rich_text_editor("Resolusi", "resolusi")

    # Fungsi untuk menggabungkan karangan
    def gabungkan_karangan():
        bahagian_plot = [
            st.session_state.get("hasil_karangan_permulaan", ""),
            st.session_state.get("hasil_karangan_sub_konflik", ""),
            st.session_state.get("hasil_karangan_konflik", ""),
            st.session_state.get("hasil_karangan_sub_kemuncak", ""),
            st.session_state.get("hasil_karangan_kemuncak", ""),
            st.session_state.get("hasil_karangan_peleraian", ""),
            st.session_state.get("hasil_karangan_resolusi", ""),
        ]
        # Gabungkan semua bahagian dengan pemisah <br>
        karangan_gabungan = "<br>".join(bahagian_plot)
        st.session_state.hasil_karangan_gabungan = karangan_gabungan

    # Butang untuk menggabungkan karangan
    if st.button("Gabungkan Karangan"):
        gabungkan_karangan()

    # Paparkan hasil karangan gabungan
    if "hasil_karangan_gabungan" in st.session_state and st.session_state.hasil_karangan_gabungan:
        st.subheader("Hasil Karangan Gabungan")
        st.markdown(st.session_state.hasil_karangan_gabungan, unsafe_allow_html=True)

with col2:
    st.header("Tutorial")
    st.write("## Selamat Datang ke Aplikasi Penulisan Karangan")
    st.write("Gunakan editor teks di sebelah kiri untuk menulis karangan Anda.")
    st.write("Pilih teknik penulisan dari ikon di atas.")
    st.write("Klik 'Gabungkan Karangan' untuk melihat hasil gabungan.")
    
    # Video Tutorial dari YouTube
    st.write("### Video Tutorial")
    st.write("Tonton video di bawah untuk panduan lengkap:")

    # Gunakan iframe untuk memaparkan video YouTube
    video_url = "https://www.youtube.com/embed/videoseries?list=PLqlP6nt6015H6B0ybLEc_EjkjeuUqQAgE"
    components.iframe(video_url, height=300)

    # Nota tambahan
    st.write("""
    **Nota:**
    - Pastikan anda menyimpan karangan sebelum menutup aplikasi.
    - Jika anda mempunyai sebarang pertanyaan, sila rujuk video tutorial di atas.
    """)
