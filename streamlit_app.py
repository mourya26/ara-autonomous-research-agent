# streamlit_app.py

import streamlit as st
import pandas as pd
import os
import json
import sys

# Allow imports from src/
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from pdf_report import generate_pdf
from query_engine import run_pandas_code
from llm_wrapper import ask_for_pandas_code
from agent import run_agent_loop


# ----------------------------------
# Session State Init
# ----------------------------------
if "df" not in st.session_state:
    st.session_state.df = None

if "final_report" not in st.session_state:
    st.session_state.final_report = None

if "run_folder" not in st.session_state:
    st.session_state.run_folder = None


# ----------------------------------
# Page setup
# ----------------------------------
st.set_page_config(page_title="ARA Autonomous Research Agent", layout="wide")
st.title("📊 ARA Autonomous Research Agent")


# ----------------------------------
# File upload
# ----------------------------------
uploaded = st.file_uploader("Upload CSV", type=["csv"])
iterations = st.number_input("Iterations", 1, 10, 3)


# ----------------------------------
# RUN AGENT
# ----------------------------------
if uploaded:
    st.session_state.df = pd.read_csv(uploaded)

    st.subheader("🔍 Preview")
    st.dataframe(st.session_state.df.head())

    if st.button("Run Agent"):
        st.info("Running...")

        result = run_agent_loop(st.session_state.df, max_iters=iterations)

        st.success("Done!")

        st.session_state.run_folder = result["run_folder"]

        # Load final report
        final_path = os.path.join(st.session_state.run_folder, "final_report.json")

        with open(final_path, "r", encoding="utf-8") as f:
            st.session_state.final_report = json.load(f)

        st.json(st.session_state.final_report)


# ----------------------------------
# PDF GENERATION (WORKS NOW)
# ----------------------------------
if st.session_state.final_report and st.session_state.run_folder:

    st.subheader("📄 Export PDF Report")

    if st.button("Generate PDF Report"):
        pdf_path = os.path.join(st.session_state.run_folder, "ARA_Report.pdf")

        plot_files = [
            os.path.join(st.session_state.run_folder, f)
            for f in os.listdir(st.session_state.run_folder)
            if f.startswith("plot_")
        ]

        generate_pdf(st.session_state.final_report, plot_files, pdf_path)

        st.success(f"PDF saved at {pdf_path}")

        with open(pdf_path, "rb") as f:
            st.download_button(
                "📥 Download PDF Report",
                f,
                file_name="ARA_Report.pdf",
                mime="application/pdf"
            )


# ----------------------------------
# OPTIONAL VISUALS
# ----------------------------------
if st.session_state.df is not None:

    st.subheader("📊 Optional Visuals")

    if st.checkbox("Correlation Heatmap"):
        import seaborn as sns
        import matplotlib.pyplot as plt

        num = st.session_state.df.select_dtypes(include=['number'])

        fig, ax = plt.subplots()
        sns.heatmap(num.corr(), annot=True, cmap="Blues", ax=ax)
        st.pyplot(fig)


# ----------------------------------
# NL → Pandas Query
# ----------------------------------
if st.session_state.df is not None:

    st.subheader("🧠 Ask a question")

    question = st.text_input("Your question")

    if st.button("Run Query"):
        code = ask_for_pandas_code(question)
        st.code(code)

        result = run_pandas_code(st.session_state.df, code)

        if result["type"] == "df":
            st.dataframe(result["data"])
        elif result["type"] == "value":
            st.write("Result:", result["data"])
        else:
            st.error(result["data"])
