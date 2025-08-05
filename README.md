# Censor Speak

**Censor Speak** is a Python-based web application that performs **speech-to-text transcription** on `.wav` audio files, detects and **censors offensive words** in both **text** and **audio** using a beep sound — just like on news channels.

Built using **Streamlit**, **Vosk**, and **PyDub**, this app allows users to:
- Transcribe audio
- Replace predefined or custom offensive words with `#@*!&`
- Censor those words in the audio using beep sounds
- Play or download the cleaned audio and transcript
---
**Demo Video**
[![Watch on YouTube](https://img.youtube.com/vi/aquua39EVKI/maxresdefault.jpg)](https://youtu.be/aquua39EVKI)

[Watch video on GitHub (censorSpeakCompressed.mp4 link)]([https://github.com/verbinden6/Censor-Speak-Audio-Transcription-Censorship/raw/main/Demo%20Video.mp4](https://github.com/verbinden6/Censor-Speak-Audio-Transcription-Censorship/blob/main/Censor%20Speak%20Compressed.mp4))


---

## ⚙️ How to Run Locally

To get started, follow these steps:

- Clone the repository:  
  `git clone https://github.com/your-username/censor-speak.git && cd censor-speak`

- Create and activate a virtual environment:  
  `python -m venv venv`

  - On **Windows**: `venv\Scripts\activate`  
  - On **macOS/Linux**: `source venv/bin/activate`

- Install the dependencies:
  - Try installing from `requirementsFinal.txt`:  
    `pip install -r requirementsFinal.txt`
  - If that doesn't work, try:  
    `pip install -r requirements.txt`
  - Or install manually:  
    `pip install streamlit vosk pydub`

- Make sure **FFmpeg** is installed and added to your system’s PATH.  
  Download from: https://ffmpeg.org/download.html

- Download the **VOSK speech recognition model** from: https://alphacephei.com/vosk/models  
  -Recommended: `vosk-model-small-en-us-0.15`  
  - Unzip it in the **project root** so the folder `vosk-model-small-en-us-0.15` is present

  Example:
  ```bash
  wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
  unzip vosk-model-small-en-us-0.15.zip

- Run the app:
  ```bash
  streamlit run app.py

---
Features
- Upload .wav audio files
- Transcribe audio to text using VOSK
- Replace offensive words in transcript with #@*!&
- Beep-censor bad words in audio
- Customize bad word list via sidebar
- Play and download censored audio
- Download censored transcript

---
Future Updates
- Real-time voice recording inside the app
- Support for .mp3 file upload and processing
- Support for Hindi and other language models
- Improved transcription with high-accuracy models
