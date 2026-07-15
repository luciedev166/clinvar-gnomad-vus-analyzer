"""Load the Phase 4 app dataset for the Streamlit app.

Kept separate from app.py (and free of any Streamlit import) so it can be
tested or reused without spinning up the app.
"""

from pathlib import Path

import pandas as pd

# app.py lives at the project root, and this file lives in src/, so
# going up one level from here gets us back to the project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "atm_vus_app_dataset.csv"

# These columns hold whole numbers but can contain missing values
# (protein_position is null for the 8 "Needs review" rows). Plain
# pd.read_csv would load them as float64, which prints as "13.0"
# instead of "13". Int64 (capital I = pandas' nullable integer type)
# keeps them looking like integers while still allowing <NA>.
NULLABLE_INT_COLUMNS = ["clinvar_variation_id", "protein_position"]

# Saved to CSV as plain "YYYY-MM-DD" text; read back in as a real
# datetime so the app can sort/format it consistently.
DATE_COLUMNS = ["clinvar_last_evaluated"]


def load_app_dataset(path: Path = DATA_PATH) -> pd.DataFrame:
    """Read atm_vus_app_dataset.csv and restore its intended dtypes."""
    if not path.exists():
        raise FileNotFoundError(
            f"App dataset not found at {path}. Run notebooks/04_build_app_dataset.ipynb first."
        )

    df = pd.read_csv(path)

    for column in NULLABLE_INT_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")

    for column in DATE_COLUMNS:
        df[column] = pd.to_datetime(df[column], errors="coerce")

    return df
