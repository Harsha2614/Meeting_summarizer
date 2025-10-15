# 🎤 Meeting Summarizer (FastAPI + OpenAI + MySQL)

An AI-powered **Meeting Summarizer** that transcribes and summarizes your meeting recordings automatically.  
Built with **FastAPI**, **OpenAI Whisper**, and **GPT-4o-mini**, it provides instant transcripts, concise summaries, and stores results in a **MySQL database** — all through a clean, minimal frontend.

---

## 🚀 Features

- 🎧 **Speech-to-Text**: Converts MP3/WAV audio into accurate transcripts using OpenAI Whisper.
- 🧠 **AI Summarization**: Generates quick and structured meeting summaries using GPT-4o-mini.
- 💾 **MySQL Integration**: Stores transcripts and summaries for later retrieval.
- ⚡ **Fast & Simple UI**: Pure HTML + JavaScript frontend for quick testing.
- 🔁 **Persistent History**: Browse and view all previously uploaded meetings.

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | FastAPI (Python 3.10+) |
| **AI Models** | OpenAI Whisper (ASR), GPT-4o-mini (LLM) |
| **Database** | MySQL |
| **Frontend** | HTML, CSS, Vanilla JS |
| **Env Management** | python-dotenv |
| **Server** | Uvicorn |

---

## 🗂️ Project Structure

meeting_summarizer/
│

├── backend/

│ ├── app.py # FastAPI main server

│ ├── asr_service.py # Audio transcription logic (Whisper)

│ ├── llm_service.py # AI summarization logic (GPT-4o)

│ ├── uploads/ # Uploaded audio files

│ ├── .env # Environment variables

│ └── requirements.txt

│
└── frontend/

└── index.html # UI for upload + results


---

## ⚙️ Installation

### 1️⃣ Clone the repository

git clone https://github.com/Harsha2614/meeting-summarizer.git

cd meeting-summarizer/backend

### 2️⃣ Create a virtual environment

python -m venv .venv

.venv\Scripts\activate  # (Windows)

### 3️⃣ Install dependencies

pip install --upgrade pip

pip install -r requirements.txt

Example requirements.txt:

fastapi
uvicorn
python-dotenv
aiofiles
openai>=1.35.14
mysql-connector-python
ffmpeg-python
tqdm

#🔑 Environment Variables

Create a .env file inside your backend/ folder:

OPENAI_API_KEY=your_openai_api_key_here
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=meeting_summarizer
STORAGE_DIR=uploads


# 🏃 Run the Application

## 1️⃣ Start the FastAPI backend

cd backend

python -m uvicorn app:app --reload

## 2️⃣ Open the frontend

Just open frontend/index.html in your browser.

# 🧠 How It Works

Upload an MP3/WAV file from the frontend.

FastAPI sends the audio to OpenAI Whisper → gets a transcript.

The transcript is summarized via GPT-4o-mini → concise, readable summary.

Both transcript & summary are stored in MySQL.

The frontend displays the full summary instantly and lists previous uploads.

# 💡 Future Enhancements

Multi-speaker diarization

PDF summary export

Email/share summary feature

Web dashboard with user login

# 🧑‍💻 Author

Narayana Harsha Vardhan

Email: harsha.rmb31@gmail.com


