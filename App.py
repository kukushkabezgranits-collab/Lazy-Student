import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Lazy Student", page_icon="😴")
st.title("Lazy Student 😴")
st.caption("Record or upload a lecture and get the typed version.")

# API key is stored in Streamlit secrets (never put it in the code)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

LANGUAGES = {
    "Auto-detect": None,
    "English": "en",
    "Russian": "ru",
    "Hindi": "hi",
    "Urdu": "ur",
    "Arabic": "ar",
    "Spanish": "es",
    "French": "fr",
}
lang_name = st.selectbox("Lecture language", list(LANGUAGES.keys()))
lang = LANGUAGES[lang_name]

tab_rec, tab_up = st.tabs(["🎙️ Record", "📁 Upload"])
with tab_rec:
    recorded = st.audio_input("Tap to record the lecture")
with tab_up:
    uploaded = st.file_uploader(
        "Upload audio", type=["mp3", "wav", "m4a", "mp4", "webm", "ogg"]
    )

audio = recorded or uploaded

if audio and st.button("Transcribe", type="primary"):
    with st.spinner("Typing your lecture..."):
        try:
            kwargs = {"model": "whisper-1", "file": audio}
            if lang:
                kwargs["language"] = lang
            result = client.audio.transcriptions.create(**kwargs)
            st.session_state["text"] = result.text
        except Exception as e:
            st.error(f"Something went wrong: {e}")

if "text" in st.session_state:
    st.subheader("Your notes")
    text = st.text_area("Edit if needed", st.session_state["text"], height=300)
    st.download_button("Download as .txt", text, file_name="lecture_notes.txt")
    
