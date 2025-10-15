import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def summarize_transcript(transcript: str) -> str:
    """
    Fast summarization using GPT-4o-mini (no chunking).
    Produces concise summaries for quick response times.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "[SUMMARY-FAILED] OPENAI_API_KEY not set."

    # ✅ Set OpenAI API key globally
    openai.api_key = api_key

    if len(transcript.strip()) < 50:
        return "Transcript too short for summarization."

    try:
        print("⚡ Generating summary quickly (no chunking)...")

        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # Fast and accurate model
            messages=[
                {"role": "system", "content": "You are an efficient and precise meeting summarizer."},
                {"role": "user", "content": f"Please summarize this meeting concisely:\n\n{transcript}"}
            ],
            max_tokens=400,  # Enough for short, focused summaries
            temperature=0.4,  # Low = factual, less creative
        )

        summary = response.choices[0].message.content.strip()
        print("✅ Summary generated successfully.")
        return summary

    except Exception as e:
        print("❌ Summarization failed:", e)
        return f"[SUMMARY-ERROR] {str(e)}"
