# 📊 ARA – Autonomous Research Agent

*LLM-Driven Data Analysis System using Gemini + Streamlit*

ARA (Autonomous Research Agent) is an intelligent, multi-iteration data-analysis assistant that automatically performs EDA, generates hypotheses, proposes experiments, and suggests diagnostics using Gemini AI — all *without executing unsafe code*.

This project provides a complete workflow where a user can:

- Upload a CSV  
- Run an AI-powered research loop  
- View hypotheses & experiment plans  
- Explore visual analytics  
- Export the results as a professional PDF report  

---

## 🚀 Features

### ✅ 1. Autonomous Research Loop

The agent performs multiple iterations of:

- Hypothesis generation  
- Experiment proposal  
- Diagnostics suggestions (safe Pandas code)  
- EDA-aware reasoning  
- Memory across iterations (context-aware)  

All results are saved to a structured folder:

```text
runs/<timestamp>/
```
---

## ✅ 2. Streamlit Frontend

A full interactive dashboard where users can:

Upload CSV files

Run the Autonomous Research Agent

View structured JSON output

Browse hypotheses, experiments, and diagnostics

Optionally visualize heatmaps, distributions, and risk-level insights

Ask natural-language data questions → auto-generated Pandas code

Export a polished PDF report

---

## ✅ 3. PDF Report Generator

Creates a professional analysis report including:

Dataset summary

Column data types

Agent history (all iterations)

Hypotheses + Experiments

Diagnostics (as readable code blocks)

Embedded plots (if generated)

---

## ✅ 4. Secure by Design

No code execution directly from the LLM

Diagnostics returned as plain strings

Only controlled Pandas execution inside a sandbox

.env for API key handling

.gitignore to protect secrets and artifacts

---

## 🧠 Architecture Overview

ara-project/

│

├── streamlit_app.py        # UI dashboard

├── requirements.txt        # Dependencies

├── .env                    # API keys (ignored in repo)

│

├── src/

│   ├── agent.py            # Multi-iteration research loop

│   ├── eda.py              # Quick EDA summary generator

│   ├── llm_wrapper.py      # Gemini API wrapper (JSON-only mode)

│   ├── pdf_report.py       # PDF exporter (ReportLab)

│   ├── query_engine.py     # Safe Pandas execution

│   └── ...

│

├── data/

│   └── sample.csv          # Example dataset

│

├── runs/                   # Auto-created folders for each execution (git-ignored)

└── Readme.md
---

## 🛠 Tech Stack
Core
- Python
- Pandas
- Google Gemini 2.0 Flash
- Streamlit
- ReportLab (PDF generation)

AI
- Iterative LLM-driven reasoning
- JSON-only controlled outputs
- Safe Pandas execution

Visuals
- Seaborn
- Matplotlib
- Built-in Streamlit rendering

---

## 📥 Installation

1. Clone the repo
```
git clone https://github.com/mourya26/ara-autonomous-research-agent.git
cd ara-autonomous-research-agent
```

2. Create virtual environment
```
python -m venv .venv
.venv\Scripts\activate
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. Add your API key
Create a .env file in the project root:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```
---

▶ Run the App
```
streamlit run streamlit_app.py
```
Then open your browser at:
```
http://localhost:8501
```

---

## 📊 Usage Workflow

1. Upload a CSV
   - Any dataset works: finance, HR, retail, transactions, sensors, logs, etc.

2. Select number of iterations
   - More iterations → deeper reasoning.

3.  Run the agent

    -   The app will produce:

    -   Hypotheses

    -   Experiment plans

    -   Diagnostics (Pandas code)

    -   Insights across iterations

4.  Explore visuals

    -   Optional built-in analytics:

    -   Heatmaps

    -   Distributions

    -   Risk-level breakdowns

    -   Interactive charts

5. Export to PDF
  - Get a professional report ready to share.

---

## 📄 Sample Output

The agent generates structured research like:
```
{
  "iteration": 3,
  "hypotheses": [
    "Expenses with missing rule_flags have higher risk profiles",
    "Specific vendors consistently exhibit abnormal behavior"
  ],
  "experiment": "Analyze category/vendor combinations and compare average risk",
  "diagnostics": [
    "df['rule_flags'].isnull().sum()",
    "df.groupby('vendor_id')['final_risk_score'].mean().head(10)"
  ]
}
```

---

## 🗺 Future Enhancements

LangGraph / AutoGen agent orchestration

Multi-agent reasoning

RAG over historical runs

SQL mode (for database datasets)

Model selection (Flash / Pro / Flash Thinking)

Cloud deployment (GCP / AWS / Azure)

