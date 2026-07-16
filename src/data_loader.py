from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "atm_vus_app_dataset.csv"
NULLABLE_INT_COLUMNS = ["clinvar_variation_id", "protein_position"]

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
