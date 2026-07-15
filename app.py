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
