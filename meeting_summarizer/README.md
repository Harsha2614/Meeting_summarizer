# Meeting Summarizer

**Objective:** Transcribe meeting audio and generate action-oriented summaries and action items.

## What is included
- `backend/` — FastAPI backend with endpoints to upload audio, retrieve transcripts and summaries.
- `frontend/index.html` — Simple static demo UI to upload audio and view results.
- `.env.example` — Environment variable examples
- `requirements.txt` for backend dependencies.

## Setup (Backend)
1. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.
2. Create a Python virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
```

3. Run the backend:
```bash
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

4. Open `frontend/index.html` in your browser (or serve it with a static server), choose an audio file and click **Upload & Process**.

## How it works
- The backend saves uploaded audio to `uploads/`.
- `asr_service.transcribe_file` will call OpenAI Whisper if `OPENAI_API_KEY` is set. Replace with your preferred ASR if needed.
- `llm_service.summarize_transcript` will call OpenAI ChatCompletion to summarize the transcript.

## Notes & Tips
- For higher transcription accuracy, consider using Google Speech-to-Text or a hosted Whisper instance.
- Add speaker diarization as a future enhancement (e.g., PyAnnote or assemblyai).
- To demo without API keys, the services return descriptive error messages telling you to set `OPENAI_API_KEY`.

## Deliverables for submission
- Zip file (this repository)
- GitHub repo with the same structure
- Demo video (screen-record showing upload -> transcript -> summary)
