# src/agent.py

import os
import sys
import json
from datetime import datetime
import pandas as pd
from llm_wrapper import call_llm
from eda import quick_eda  

# Robust JSON helper
def safe_parse_json(text):
    """
    Try to parse JSON from model output.
    1) Direct json.loads
    2) Extract first {...} block and parse that
    3) Try cleaning obvious trailing commas
    """
    if not isinstance(text, str):
        return None

    text = text.strip()
    if not text:
        return None

    # Remove possible ```json fences
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    start = text.find("{")
    if start == -1:
        return None

    stack = []
    end = -1
    for i, ch in enumerate(text[start:], start=start):
        if ch == "{":
            stack.append("{")
        elif ch == "}":
            if stack:
                stack.pop()
                if not stack:
                    end = i
                    break

    if end == -1:
        return None

    candidate = text[start : end + 1]

    # 3) Try candidate
    try:
        return json.loads(candidate)
    except Exception:
        pass

    # 4) Clean trailing commas
    cleaned = candidate.replace("\t", " ")
    cleaned = cleaned.replace("\n", " ")
    cleaned = cleaned.replace(", }", " }").replace(",  }", " }")
    cleaned = cleaned.replace(", ]", " ]").replace(",  ]", " ]")

    try:
        return json.loads(cleaned)
    except Exception:
        return None

# Agent loop (Mode 2: diagnostics but no execution)
def run_agent_loop(df, max_iters=3):
    """
    Simple agent loop:
      - Compute EDA summary
      - For each iteration: ask LLM for hypotheses, diagnostics, and experiment
      - DO NOT execute diagnostics (just store them)
      - Save everything to runs/<timestamp>/final_report.json

    Returns:
      dict with keys:
        - run_folder
        - history
        - eda
    """

    # Prepare runs folder
    run_root = os.path.join(os.path.dirname(__file__), "..", "runs")
    os.makedirs(run_root, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_folder = os.path.join(run_root, timestamp)
    os.makedirs(run_folder, exist_ok=True)

    # EDA summary
    eda_text, eda_summary = quick_eda(df)

    history = []

    for iteration in range(1, max_iters + 1):
        print(f"\n=== Iteration {iteration}/{max_iters} ===")

        # Small memory: last 2 iterations
        memory_text = json.dumps(history[-2:], indent=2) if history else "[]"

        prompt = f"""
You are a data analyst.

You MUST output VALID JSON ONLY.
No markdown.
No backticks.
No comments.
No text outside JSON.

The JSON MUST have exactly these keys:
- "hypotheses": an array of strings
- "diagnostics": an array of strings (each a Python/pandas snippet, do NOT define functions)
- "experiment": a single string

If you are unsure, return empty arrays and an empty string, but keep the keys.

Example:
{{
  "hypotheses": ["Risk is correlated with amount"],
  "diagnostics": ["df['amount'].corr(df['avg_risk'])"],
  "experiment": "Compute correlation between amount and avg_risk."
}}

DATASET_EDA_SUMMARY:
{eda_text}

PAST_ITERATIONS:
{memory_text}

Now respond with ONE JSON object only.
"""

        response = call_llm(prompt)
        llm_text = response.get("text", "")

        # Save raw model output for debugging
        raw_path = os.path.join(run_folder, f"iter{iteration}_raw.txt")
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(llm_text)

        parsed = safe_parse_json(llm_text)

        if parsed is None or not isinstance(parsed, dict):
            # record error and stop
            history.append(
                {
                    "iteration": iteration,
                    "error": "LLM returned invalid JSON",
                    "raw_snippet": llm_text[:500],
                }
            )
            break

        entry = {
            "iteration": iteration,
            "hypotheses": parsed.get("hypotheses", []),
            "experiment": parsed.get("experiment", ""),
            "diagnostics": parsed.get("diagnostics", []),
        }
        history.append(entry)

    # Final report
    final_report = {
        "run_folder": run_folder,
        "history": history,
        "eda": eda_summary,
    }

    final_path = os.path.join(run_folder, "final_report.json")
    with open(final_path, "w", encoding="utf-8") as f:
        json.dump(final_report, f, indent=2)
    print("[agent] Completed. Final report saved at:", final_path)
    return final_report

# CLI entrypoint
if __name__ == "__main__":
    print("MAIN BLOCK IS RUNNING!")
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample.csv")
    print("Looking for:", csv_path)
    if not os.path.exists(csv_path):
        print("[ERROR] sample.csv not found at", csv_path)
        sys.exit(1)
    df = pd.read_csv(csv_path)
    print("Loaded CSV with shape:", df.shape)

    run_agent_loop(df, max_iters=3)
