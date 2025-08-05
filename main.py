import streamlit as st
from vosk import Model, KaldiRecognizer
import wave
import json
from pydub import AudioSegment
from pydub.generators import Sine
import tempfile
import os
import base64

#  Config 
MODEL_PATH = "vosk-model-small-en-us-0.15"
DEFAULT_BAD_WORDS = {"damn", "hell", "shit", ""}

# Load model 
if not os.path.exists(MODEL_PATH):
    st.error("VOSK model not found. Please unzip it into this folder.")
    st.stop()

model = Model(MODEL_PATH)

#  Helper Functions 
def transcribe(audio_path):
    wf = wave.open(audio_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            if "result" in res:
                results.extend(res["result"])
    res = json.loads(rec.FinalResult())
    if "result" in res:
        results.extend(res["result"])
    wf.close()
    full_text = " ".join([w["word"] for w in results])
    return full_text, results

def censor_text(text, bad_words):
    return " ".join(["#@*!&" if w.lower() in bad_words else w for w in text.split()])

def censor_audio(audio_path, timestamps, bad_words):
    sound = AudioSegment.from_wav(audio_path)
    censored = sound
    for word in timestamps:
        if word["word"].lower() in bad_words:
            start = int(word["start"] * 1000)
            end = int(word["end"] * 1000)
            duration = end - start
            beep = Sine(1000).to_audio_segment(duration=duration).apply_gain(-3)
            censored = censored[:start] + beep + censored[end:]
    censored_path = tempfile.mktemp(suffix=".mp3")
    censored.export(censored_path, format="mp3")
    return censored_path

def get_download_link(file_path, label):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:audio/mp3;base64,{b64}" download="{os.path.basename(file_path)}" style="text-decoration:none;font-weight:bold;color:white;background-color:#4CAF50;padding:8px 12px;border-radius:4px;">{label}</a>'
    return href

# Streamlit UI 
st.set_page_config(page_title="🔇 Speech Censorship", page_icon="🎤", layout="centered")
st.sidebar.markdown(" Settings")
custom_words = st.sidebar.text_input("Bad words (comma-separated)", ", ".join(DEFAULT_BAD_WORDS), help="Add words to censor, separated by commas.")
BAD_WORDS = set(w.strip().lower() for w in custom_words.split(",") if w.strip())

st.markdown("""
    <style>
        .app-title {
            font-size: 3rem;
            font-weight: 800;
            color: white;
            margin-bottom: 1.2rem;
        }
        .app-subtitle {
            font-size: 2rem;
            font-weight: 500;
            color: white;
            margin-bottom: 1rem;
        }
        .app-subtitle2 {
            font-size: 1.6rem;
            font-weight: 500;
            color: white;
            margin-bottom: 1rem;
        }
        .app-instruction {
            font-size: 1.3rem;
            color: white;
            margin-bottom: 2rem;
        }
    </style>

    <div class="app-title">🔇 Censor Speak</div>
    <div class="app-subtitle"> Audio Transcription & Censorship</div>
    <div class="app-subtitle2">Beep out the bad — keep the rest</div>
    <div class="app-instruction">Upload audio •  Transcribe  •  Censor  •  Play &  Download</div>
""", unsafe_allow_html=True)


#  Upload Audio 
audio_path = None
uploaded_file = st.file_uploader("Upload a WAV audio file", type=["wav"])
if uploaded_file:
    audio_path = tempfile.mktemp(suffix=".wav")
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.read())

# Process 
if audio_path:
    st.audio(audio_path, format="audio/wav")
    st.success("Audio loaded. Transcribing...")

    # Transcribe and censor
    transcribed_text, word_data = transcribe(audio_path)
    censored_text = censor_text(transcribed_text, BAD_WORDS)
    censored_audio_path = censor_audio(audio_path, word_data, BAD_WORDS)

    # Display Results
    st.subheader("Transcribed Text")
    st.text_area("Original", value=transcribed_text, height=200, key="transcribed", label_visibility="collapsed")

    st.subheader("Censored Text")
    st.text_area("Censored", value=censored_text, height=200, key="censored", label_visibility="collapsed")

    st.subheader("Censored Audio")
    st.audio(censored_audio_path, format="audio/mp3")
    st.markdown(get_download_link(censored_audio_path, "⬇️ Download Censored Audio (.mp3)"), unsafe_allow_html=True)

    st.download_button("⬇Download Censored Transcript (.txt)", data=censored_text, file_name="censored_text.txt")

# Bottom Footer Centered 
st.markdown("""
    <style>
    .footer-container {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        padding: 10px 0;
        text-align: center;
        z-index: 9999;
    }
    .footer-text {
        font-size: 1rem;
        color: white;
    }
    </style>

    <div class="footer-container">
        <div class="footer-text">&lt;/&gt;  Aditya Gupta</div>
    </div>
""", unsafe_allow_html=True)



