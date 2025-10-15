import os
import uuid
import mysql.connector
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import aiofiles
from dotenv import load_dotenv

# Import services
from asr_service import transcribe_file
from llm_service import summarize_transcript

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "meeting_summarizer")
STORAGE_DIR = os.getenv("STORAGE_DIR", "uploads")

os.makedirs(STORAGE_DIR, exist_ok=True)

# -------------------------
# Connect to MySQL
# -------------------------
def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id VARCHAR(255) PRIMARY KEY,
            filename VARCHAR(255),
            uploaded_at DATETIME,
            transcript LONGTEXT,
            summary LONGTEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("📁 MySQL database initialized successfully.")

init_db()

# -------------------------
# FastAPI App
# -------------------------
app = FastAPI(title="Meeting Summarizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if OPENAI_API_KEY:
    print("✅ OpenAI API Key loaded successfully.")
else:
    print("❌ ERROR: OPENAI_API_KEY not loaded! Check .env file placement and syntax.")

# -------------------------
# API Endpoints
# -------------------------
@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    """Upload, transcribe, summarize, and store results in MySQL."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    meeting_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]
    dest_filename = f"{meeting_id}{ext}"
    dest_path = os.path.join(STORAGE_DIR, dest_filename)

    print(f"⬆️ Uploading file: {file.filename} → {dest_path}")

    async with aiofiles.open(dest_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    # Transcribe audio
    print("🎧 Starting transcription...")
    transcript = transcribe_file(dest_path)
    print("📝 Transcript ready.")

    # Summarize text
    print("💡 Generating summary...")
    summary = summarize_transcript(transcript)
    print("✅ Summary complete.")

    # Store results in MySQL
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO meetings (id, filename, uploaded_at, transcript, summary)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (meeting_id, dest_filename, datetime.utcnow(), transcript, summary)
        )
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MySQL error: {e}")
    finally:
        cursor.close()
        conn.close()

    return JSONResponse({
        "id": meeting_id,
        "filename": dest_filename,
        "transcript": transcript,
        "summary": summary,
        "message": "✅ Audio processed and stored successfully!"
    })


@app.get("/list")
def list_meetings():
    """List all stored meetings."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, filename, uploaded_at FROM meetings ORDER BY uploaded_at DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"meetings": rows}


@app.get("/summary/{meeting_id}")
def get_summary(meeting_id: str):
    """Fetch transcript & summary by meeting ID."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT transcript, summary FROM meetings WHERE id = %s", (meeting_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return row
