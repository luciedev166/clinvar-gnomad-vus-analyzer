import pandas as pd
import streamlit as st

from src.data_loader import load_app_dataset

st.set_page_config(
    page_title="ATM ClinVar + gnomAD VUS Explorer",
    layout="wide",
)

st.title("ATM ClinVar + gnomAD VUS Explorer")
st.caption(
    "Explore ATM missense variants of uncertain significance (VUS) using "
    "ClinVar clinical annotations and gnomAD population-frequency evidence."
)

st.warning(
    "**Educational tool only \u2014 not a diagnostic device.** This app presents "
    "existing public evidence from ClinVar and gnomAD. It does not diagnose, "
    "reclassify variants, or provide clinical recommendations. Any questions "
    "about a specific variant or result should go to a qualified clinician "
    "or genetic counselor.",
    icon="\u26a0\ufe0f",
)


@st.cache_data
def get_dataset():
    return load_app_dataset()


df = get_dataset()

total_variants = len(df)
matched_count = (df["gnomad_match_status"] == "Matched").sum()
unmatched_count = (df["gnomad_match_status"] == "Not found in gnomAD").sum()
parsed_count = (df["protein_parse_status"] == "Parsed").sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total VUS candidates", f"{total_variants:,}")
col2.metric("Matched in gnomAD", f"{matched_count:,}")
col3.metric("Not found in gnomAD", f"{unmatched_count:,}")
col4.metric("Protein changes parsed", f"{parsed_count:,}")


# Columns checked by the single search box.
SEARCH_COLUMNS = [
    "protein_change",
    "clinvar_variation_id",
    "rs_id",
    "vcv_accession",
    "variant_id",
]


@st.cache_data
def get_condition_options(df: pd.DataFrame) -> list[str]:
    """Split the comma-separated `condition` column into individual,
    de-duplicated condition names for the filter dropdown."""
    conditions = set()
    for value in df["condition"].dropna():
        for part in value.split(","):
            part = part.strip()
            if part:
                conditions.add(part)
    return sorted(conditions)


def filter_dataset(
    df: pd.DataFrame,
    search_text: str,
    match_statuses: list[str],
    review_statuses: list[str],
    conditions: list[str],
    af_range: tuple[float, float],
) -> pd.DataFrame:
    """Apply the sidebar's search box and filters to the dataset.

    Kept as a plain function (df and values in, filtered df out) rather
    than reading widget state directly, so it can be tested without
    Streamlit and reused if we add more entry points later.
    """
    filtered = df

    if search_text.strip():
        needle = search_text.strip().lower()
        mask = pd.Series(False, index=filtered.index)
        for column in SEARCH_COLUMNS:
            mask |= (
                filtered[column]
                .astype("string")
                .str.lower()
                .str.contains(needle, na=False)
            )
        filtered = filtered[mask]

    if match_statuses:
        filtered = filtered[filtered["gnomad_match_status"].isin(match_statuses)]

    if review_statuses:
        filtered = filtered[filtered["review_status"].isin(review_statuses)]

    if conditions:
        condition_text = filtered["condition"].fillna("")
        condition_mask = condition_text.apply(
            lambda value: any(condition in value for condition in conditions)
        )
        filtered = filtered[condition_mask]

    min_af, max_af = af_range
    af_mask = filtered["gnomad_af"].isna() | filtered["gnomad_af"].between(
        min_af, max_af
    )
    filtered = filtered[af_mask]

    return filtered


st.sidebar.header("Search & filter")

search_text = st.sidebar.text_input(
    "Search",
    placeholder="Protein change, Variation ID, rsID, VCV accession, or variant_id",
)

match_status_options = sorted(df["gnomad_match_status"].unique())
selected_match_statuses = st.sidebar.multiselect(
    "gnomAD match status",
    options=match_status_options,
    default=match_status_options,
)

review_status_options = sorted(df["review_status"].unique())
selected_review_statuses = st.sidebar.multiselect(
    "Review status",
    options=review_status_options,
    default=review_status_options,
)

condition_options = get_condition_options(df)
selected_conditions = st.sidebar.multiselect("Condition", options=condition_options)

max_af = float(df["gnomad_af"].max())
af_range = st.sidebar.slider(
    "gnomAD allele frequency",
    min_value=0.0,
    max_value=max_af,
    value=(0.0, max_af),
    format="%.6f",
)

filtered_df = filter_dataset(
    df,
    search_text=search_text,
    match_statuses=selected_match_statuses,
    review_statuses=selected_review_statuses,
    conditions=selected_conditions,
    af_range=af_range,
)

st.subheader(f"Results ({len(filtered_df):,} variants)")
st.dataframe(filtered_df, use_container_width=True)