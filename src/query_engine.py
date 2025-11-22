import re
import sys
import io
import pandas as pd
import numpy as np

SAFE_BUILTINS = {
    "abs": abs, "min": min, "max": max, "sum": sum, "len": len, "range": range,
    "float": float, "int": int, "round": round, "print": print,
}

FORBIDDEN_SUBSTRINGS = [
    "import ", "os.", "sys.", "open(", "write(", "remove(", "delete", "drop(",
    "subprocess", "eval(", "exec(", "__"
]


def is_safe(code: str):
    c = code.lower()
    for bad in FORBIDDEN_SUBSTRINGS:
        if bad in c:
            return False, f"Blocked dangerous code: {bad}"
    return True, ""


def run_pandas_code(df: pd.DataFrame, code: str):
    """
    Executes ONLY safe Pandas/Numpy code.
    Returns dict: {type: "df"|"value"|"error", data: ...}
    """

    safe, reason = is_safe(code)
    if not safe:
        return {"type": "error", "data": reason}

    try:
        safe_globals = {
            "__builtins__": SAFE_BUILTINS,
            "pd": pd,
            "np": np
        }
        local_vars = {"df": df}

        # capture stdout
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        result = eval(code, safe_globals, local_vars)

        stdout = sys.stdout.getvalue()
        sys.stdout = old_stdout

        # convert DataFrame
        if isinstance(result, pd.DataFrame):
            return {"type": "df", "data": result}

        # convert Series
        if isinstance(result, pd.Series):
            return {"type": "df", "data": result.to_frame()}

        # everything else
        return {"type": "value", "data": result}

    except Exception as e:
        sys.stdout = old_stdout
        return {"type": "error", "data": str(e)}
