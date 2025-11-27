# src/llm_wrapper.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Try GOOGLE_API_KEY first (Gemini standard), fallback to LLM_API_KEY if present
API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("LLM_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "No API key found. Set GOOGLE_API_KEY or LLM_API_KEY in your .env file."
    )

# Configure client
genai.configure(api_key=API_KEY)

def call_llm(prompt: str, max_tokens: int = 1024):
    """
    Call Gemini 2.0 Flash and request JSON-only output.
    Returns dict: { "text": str, "raw": response, "error": optional str }
    """
    try:
        model = genai.GenerativeModel("models/gemini-2.0-flash")

        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": max_tokens,
                "response_mime_type": "application/json",  # JSON-only mode
            },
        )

        text = response.text or "{}"
        return {"text": text, "raw": response}

    except Exception as e:
        return {
            "text": "{}",
            "raw": None,
            "error": f"LLM ERROR: {e}",
        }

def ask_for_pandas_code(question: str, max_tokens: int = 256) -> str:
    """
    Ask Gemini for a SINGLE line of Pandas code that operates on an existing
    DataFrame called `df`.

    Returns a plain Python code string like:
        df['amount'].mean()
    """
    prompt = (
        "You are a data analysis assistant.\n\n"
        "You will be given a natural language question about a Pandas DataFrame named df.\n"
        "Return ONLY a single line of valid Python code using Pandas (and optionally NumPy)\n"
        "that answers the question.\n\n"
        "Requirements:\n"
        "- Use the existing variable df (do not create it).\n"
        "- Do NOT define functions or classes.\n"
        "- Do NOT import anything.\n"
        "- Do NOT create or assign to new variables.\n"
        "- Do NOT modify df in-place (no \"df[...] = ...\").\n"
        "- Do NOT include any explanations, comments, or markdown.\n"
        "- Output must NOT be wrapped in backticks.\n\n"
        "User question:\n"
        f"{question}\n\n"
        "Example good outputs:\n"
        "df['amount'].mean()\n"
        "df.groupby('category')['final_risk_score'].mean()\n\n"
        "Example bad outputs (DO NOT DO THIS):\n"
        "Here is your code: df['amount'].mean()\n"
        "```python\n"
        "df['amount'].mean()\n"
        "```\n\n"
        "Now output ONLY the code line:"
    )

    try:
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        response = model.generate_content(
            prompt,
            generation_config={"max_output_tokens": max_tokens},
        )

        text = (response.text or "").strip()
        # Strip accidental markdown fences
        text = text.replace("```python", "").replace("```", "").strip()

        # If multiple lines came back, keep the first non-empty one
        lines = [ln for ln in text.splitlines() if ln.strip()]
        return lines[0].strip() if lines else ""

    except Exception as e:
        # Fallback to something safe
        return "df.head()  # Fallback due to LLM error"
