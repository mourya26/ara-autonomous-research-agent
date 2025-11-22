from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os


def generate_pdf(report_data, plots, output_path):
    print("📄 generate_pdf STARTED")
    print("Saving to:", output_path)
    print("Plots:", plots)

    try:
        styles = getSampleStyleSheet()
        story = []

        # Title
        story.append(Paragraph("ARA Research Agent – Analysis Report", styles["Title"]))
        story.append(Spacer(1, 20))

        # --- EDA ---
        eda = report_data.get("eda", {})
        shape = eda.get("shape", [0, 0])

        story.append(Paragraph("Dataset Summary", styles["Heading2"]))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Rows: {shape[0]} &nbsp;&nbsp;&nbsp; Columns: {shape[1]}", styles["BodyText"]))
        story.append(Spacer(1, 10))

        # dtypes table
        dtypes = eda.get("dtypes", {})
        dtype_rows = [["Column", "Type"]] + [[col, typ] for col, typ in dtypes.items()]

        table = Table(dtype_rows)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ]))
        story.append(table)
        story.append(Spacer(1, 20))

        # --- History ---
        story.append(Paragraph("Agent Findings", styles["Heading2"]))
        story.append(Spacer(1, 10))

        for entry in report_data.get("history", []):
            story.append(Paragraph(f"Iteration {entry.get('iteration', '?')}", styles["Heading3"]))
            story.append(Spacer(1, 6))

            story.append(Paragraph("Hypotheses:", styles["BodyText"]))
            for h in entry.get("hypotheses", []):
                story.append(Paragraph(f"• {h}", styles["BodyText"]))
            story.append(Spacer(1, 6))

            story.append(Paragraph("Experiment:", styles["BodyText"]))
            story.append(Paragraph(entry.get("experiment", "None"), styles["BodyText"]))
            story.append(Spacer(1, 6))

            story.append(Paragraph("Diagnostics:", styles["BodyText"]))
            for d in entry.get("diagnostics", []):
                story.append(Paragraph(f"<font size=8>{d}</font>", styles["BodyText"]))
            story.append(Spacer(1, 12))

        # --- Plots ---
        if plots:
            story.append(Paragraph("Charts", styles["Heading2"]))
            story.append(Spacer(1, 10))

            for p in plots:
                if os.path.exists(p):
                    story.append(Image(p, width=400, height=250))
                    story.append(Spacer(1, 12))
                else:
                    print("⚠️ Missing plot:", p)

        # Build PDF
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        doc.build(story)

        print("📄 generate_pdf FINISHED")
        return output_path

    except Exception as e:
        print("❌ PDF GENERATION ERROR:", e)
        raise e
