import os
import ffmpeg
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def transcribe_file(file_path: str) -> str:
    """
    Fast, single-pass transcription using OpenAI Whisper (no chunking).
    Best for short/medium audio files — returns full transcript quickly.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "[TRANSCRIPTION-FAILED] OPENAI_API_KEY not set."

    # ✅ Set OpenAI API key globally
    openai.api_key = api_key

    try:
        print(f"🎙️ Sending '{os.path.basename(file_path)}' to Whisper for transcription...")

        with open(file_path, "rb") as audio_file:
            result = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        transcript = result.text if hasattr(result, "text") else str(result)
        print("✅ Transcription complete.")
        return transcript.strip()

    except Exception as e:
        print("❌ Transcription failed:", e)
        return f"[TRANSCRIPTION-ERROR] {str(e)}"
