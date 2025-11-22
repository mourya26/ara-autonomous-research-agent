# src/eda.py
import pandas as pd

def quick_eda(path_or_df):
    if isinstance(path_or_df, str):
        df = pd.read_csv(path_or_df)
    else:
        df = path_or_df.copy()
    summary = {}
    summary['shape'] = df.shape
    summary['dtypes'] = df.dtypes.apply(lambda x: str(x)).to_dict()
    numeric = df.select_dtypes(include=['int','float'])
    if not numeric.empty:
        summary['numeric_describe'] = numeric.describe().to_dict()
    # simple quality checks
    summary['missing'] = df.isna().sum().to_dict()
    # return human-readable text
    text = f"Dataset shape: {summary['shape']}\n"
    text += f"Columns and types: {summary['dtypes']}\n"
    text += f"Missing values: {summary['missing']}\n"
    if 'numeric_describe' in summary:
        text += "Numeric summary (head):\n"
        for col, stats in summary['numeric_describe'].items():
            text += f" - {col}: mean={stats['mean']}, std={stats['std']}, min={stats['min']}, max={stats['max']}\n"
    return text, summary
